from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone


class Skill(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True)
    current_level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default='Beginner')
    target_level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default='Intermediate')
    confidence = models.IntegerField(default=5)
    daily_goal_minutes = models.IntegerField(default=30)
    last_practiced = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def decay_days(self):
        if not self.last_practiced:
            return 999
        return (timezone.now().date() - self.last_practiced).days

    def decay_status(self):
        days = self.decay_days()
        if days <= 3:
            return 'Healthy'
        if days <= 7:
            return 'Stable'
        if days <= 14:
            return 'Needs Practice'
        if days <= 30:
            return 'At Risk'
        return 'Critical'

    def progress_percent(self):
        level_order = {'Beginner': 30, 'Intermediate': 60, 'Advanced': 90}
        current = level_order.get(self.current_level, 30)
        target = level_order.get(self.target_level, 90)
        return max(10, min(100, int((current + target) / 2)))

    def total_minutes(self):
        total = self.sessions.aggregate(total=Sum('duration_minutes'))['total'] or 0
        return int(total)

    def estimate_days_to_target(self):
        progress = self.progress_percent()
        if progress >= 100:
            return 0
        return max(7, int((100 - progress) / max(self.confidence, 1)) + 7)


class PracticeSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practice_sessions')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='sessions')
    topic = models.CharField(max_length=200)
    duration_minutes = models.IntegerField(default=0)
    confidence = models.IntegerField(default=5)
    notes = models.TextField(blank=True)
    practiced_at = models.DateField(default=date.today)

    def __str__(self):
        return f'{self.skill.name} - {self.topic}'


class AISummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_summaries')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='ai_summaries', null=True, blank=True)
    summary = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.summary[:80]
