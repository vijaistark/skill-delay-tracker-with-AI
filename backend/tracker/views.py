import json
import os
from datetime import timedelta
from urllib import request, error

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Skill, PracticeSession, AISummary
from .serializers import SkillSerializer, PracticeSessionSerializer, AISummarySerializer, UserSerializer


UserModel = get_user_model()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please enter a username and password.'}, status=400)

    if UserModel.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=400)

    user = UserModel.objects.create_user(username=username, email=email, password=password)
    refresh = RefreshToken.for_user(user)
    return Response({
        'user': UserSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=201)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = UserModel.objects.filter(username=username).first()
    if user is None or not user.check_password(password):
        return Response({'error': 'Invalid username or password.'}, status=400)

    refresh = RefreshToken.for_user(user)
    return Response({
        'user': UserSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


class SkillListCreateView(generics.ListCreateAPIView):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Skill.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Skill.objects.filter(user=self.request.user)


class PracticeSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = PracticeSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PracticeSession.objects.filter(user=self.request.user).order_by('-practiced_at', '-id')

    def perform_create(self, serializer):
        skill = serializer.validated_data['skill']
        if skill.user != self.request.user:
            raise PermissionError('You cannot add sessions for another user.')
        session = serializer.save(user=self.request.user)
        skill.last_practiced = session.practiced_at
        skill.confidence = session.confidence
        skill.save(update_fields=['last_practiced', 'confidence'])

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except PermissionError:
            return Response({'error': 'You cannot add sessions for another user.'}, status=403)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard(request):
    skills = Skill.objects.filter(user=request.user)
    total_minutes = PracticeSession.objects.filter(user=request.user).aggregate(total=Sum('duration_minutes'))['total'] or 0
    streak_days = calculate_streak(request.user)

    serialized = []
    for skill in skills:
        serialized.append({
            **SkillSerializer(skill).data,
            'streak': calculate_streak_for_skill(skill),
            'decay_status': skill.decay_status(),
            'progress_percent': skill.progress_percent(),
            'total_minutes': skill.total_minutes(),
        })

    return Response({
        'total_minutes': total_minutes,
        'streak_days': streak_days,
        'skills': serialized,
    })


def build_local_summary(skill, streak_days, recent_days, average_minutes, estimate_days):
    if streak_days >= 7:
        tone = f"You've built a {streak_days}-day streak with {skill.name}. "
    elif streak_days >= 3:
        tone = f"Your {skill.name} practice has been steady, with a {streak_days}-day streak. "
    else:
        tone = f"You are still building a routine for {skill.name}. "

    return (
        f"{tone}You have practiced on {recent_days} recent days and averaged about {int(average_minutes)} minutes per active day. "
        f"Your current pace suggests you could make meaningful progress toward your {skill.target_level} goal in approximately {estimate_days} days if you keep the routine going."
    )


def generate_ai_text(skill, streak_days, recent_days, average_minutes, estimate_days):
    api_key = os.getenv('LLM_API_KEY')
    api_url = os.getenv('LLM_API_URL', 'https://api.openai.com/v1/chat/completions')
    if not api_key:
        return build_local_summary(skill, streak_days, recent_days, average_minutes, estimate_days)

    prompt = (
        f"You are a supportive learning coach. Write a short, encouraging summary in 2 to 3 sentences. "
        f"The user's skill is {skill.name}. Their current level is {skill.current_level}. Their target is {skill.target_level}. "
        f"They have a {streak_days}-day streak, practiced on {recent_days} recent days, averaged {int(average_minutes)} minutes per active day, "
        f"and the calculated estimate is approximately {estimate_days} days to reach the target pace. "
        f"Do not claim exact mastery. Mention the estimate as an approximation."
    )

    payload = {
        'model': os.getenv('LLM_MODEL', 'gpt-4o-mini'),
        'messages': [
            {'role': 'system', 'content': 'You help people maintain a technical learning routine. Keep the answer short, realistic, and encouraging.'},
            {'role': 'user', 'content': prompt},
        ],
        'temperature': 0.7,
    }

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    try:
        req = request.Request(api_url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            content = data.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
            if content:
                return content
    except (error.HTTPError, error.URLError, ValueError, TypeError, KeyError):
        pass

    return build_local_summary(skill, streak_days, recent_days, average_minutes, estimate_days)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generate_ai_summary(request):
    skill_id = request.data.get('skill_id')
    skill = Skill.objects.filter(user=request.user, id=skill_id).first() if skill_id else Skill.objects.filter(user=request.user).order_by('-last_practiced').first()

    if not skill:
        return Response({'error': 'Please add a skill first.'}, status=400)

    sessions = PracticeSession.objects.filter(user=request.user, skill=skill)
    total_minutes = sessions.aggregate(total=Sum('duration_minutes'))['total'] or 0
    recent_days = sessions.values_list('practiced_at', flat=True).distinct().count()
    streak_days = calculate_streak_for_skill(skill)
    average = total_minutes / max(recent_days, 1)
    estimate = skill.estimate_days_to_target()
    summary = generate_ai_text(skill, streak_days, recent_days, average, estimate)

    ai_summary = AISummary.objects.create(user=request.user, skill=skill, summary=summary)
    return Response(AISummarySerializer(ai_summary).data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def recommendations(request):
    skills = Skill.objects.filter(user=request.user).order_by('last_practiced')
    if not skills:
        return Response({
            'today_focus': None,
            'reason': 'Add a skill to start tracking your learning.',
            'suggested_duration': 30,
            'summary': 'Start with a short daily session to build momentum.'
        })

    focus_skill = skills.first()
    today = __import__('datetime').date.today()
    days_since = (today - (focus_skill.last_practiced or today)).days if focus_skill.last_practiced else 999

    if days_since >= 10:
        reason = f"You haven't practiced {focus_skill.name} for {days_since} days."
        suggested_duration = max(focus_skill.daily_goal_minutes // 2, 20)
        summary = f"Your {focus_skill.name} activity has decreased recently. A short daily session can help rebuild consistency."
    else:
        reason = f"You are keeping a steady rhythm with {focus_skill.name}."
        suggested_duration = focus_skill.daily_goal_minutes
        summary = f"Your {focus_skill.name} momentum is stable. Keeping your current routine will help maintain progress."

    return Response({
        'today_focus': focus_skill.name,
        'reason': reason,
        'suggested_duration': suggested_duration,
        'summary': summary,
    })


def calculate_streak(user):
    session_days = sorted(
        set(PracticeSession.objects.filter(user=user).values_list('practiced_at', flat=True)),
        reverse=True,
    )
    if not session_days:
        return 0

    today = __import__('datetime').date.today()
    current = today
    streak = 0

    for session_day in session_days:
        if session_day == current:
            streak += 1
            current -= timedelta(days=1)
        elif session_day == current - timedelta(days=1):
            streak += 1
            current -= timedelta(days=1)
        else:
            break

    return streak


def calculate_streak_for_skill(skill):
    session_days = sorted(
        set(PracticeSession.objects.filter(skill=skill).values_list('practiced_at', flat=True)),
        reverse=True,
    )
    if not session_days:
        return 0

    today = __import__('datetime').date.today()
    current = today
    streak = 0

    for session_day in session_days:
        if session_day == current:
            streak += 1
            current -= __import__('datetime').timedelta(days=1)
        elif session_day == current - __import__('datetime').timedelta(days=1):
            streak += 1
            current -= __import__('datetime').timedelta(days=1)
        else:
            break

    return streak
