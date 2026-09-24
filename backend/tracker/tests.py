from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from .models import PracticeSession, Skill
from .views import calculate_streak


class SkillTrackingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='secret123')
        self.skill = Skill.objects.create(
            user=self.user,
            name='Python',
            category='Programming',
            current_level='Beginner',
            target_level='Advanced',
            confidence=6,
            daily_goal_minutes=45,
        )

    def test_decay_status_healthy_for_recent_practice(self):
        self.skill.last_practiced = date.today()
        self.skill.save()
        self.assertEqual(self.skill.decay_status(), 'Healthy')

    def test_streak_counts_consecutive_days(self):
        PracticeSession.objects.create(
            user=self.user,
            skill=self.skill,
            topic='Functions',
            duration_minutes=30,
            confidence=8,
            practiced_at=date.today(),
        )
        PracticeSession.objects.create(
            user=self.user,
            skill=self.skill,
            topic='Loops',
            duration_minutes=40,
            confidence=7,
            practiced_at=date.today() - timedelta(days=1),
        )

        self.assertEqual(calculate_streak(self.user), 2)
