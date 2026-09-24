from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Skill, PracticeSession, AISummary


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class SkillSerializer(serializers.ModelSerializer):
    decay_status = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()
    streak = serializers.SerializerMethodField()
    total_minutes = serializers.SerializerMethodField()
    estimate_days_to_target = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = [
            'id', 'user', 'name', 'category', 'current_level', 'target_level',
            'confidence', 'daily_goal_minutes', 'last_practiced', 'created_at',
            'decay_status', 'progress_percent', 'streak', 'total_minutes',
            'estimate_days_to_target'
        ]
        read_only_fields = ['user', 'created_at', 'last_practiced', 'decay_status', 'progress_percent', 'streak', 'total_minutes', 'estimate_days_to_target']

    def get_decay_status(self, obj):
        return obj.decay_status()

    def get_progress_percent(self, obj):
        return obj.progress_percent()

    def get_streak(self, obj):
        from .views import calculate_streak_for_skill
        return calculate_streak_for_skill(obj)

    def get_total_minutes(self, obj):
        return obj.total_minutes()

    def get_estimate_days_to_target(self, obj):
        return obj.estimate_days_to_target()

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Please enter a skill name.')
        return value.strip()

    def validate_confidence(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Confidence must be between 1 and 10.')
        return value


class PracticeSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeSession
        fields = ['id', 'user', 'skill', 'topic', 'duration_minutes', 'confidence', 'notes', 'practiced_at']
        read_only_fields = ['user']

    def validate_duration_minutes(self, value):
        if value <= 0:
            raise serializers.ValidationError('Please enter a duration greater than zero.')
        return value

    def validate_confidence(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Confidence must be between 1 and 10.')
        return value


class AISummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = AISummary
        fields = ['id', 'user', 'skill', 'summary', 'generated_at']
        read_only_fields = ['user', 'generated_at']
