from datetime import timedelta

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    title = models.CharField(max_length=120)
    reason = models.CharField(max_length=255, blank=True, help_text='Why is this habit important?')
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def current_streak(self):
        """Return consecutive completed days ending today."""
        day = timezone.localdate()
        streak = 0
        completed_dates = set(
            self.progress_entries.filter(done=True).values_list('date', flat=True)
        )

        while day in completed_dates:
            streak += 1
            day -= timedelta(days=1)
        return streak


class Progress(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='progress_entries')
    date = models.DateField(default=timezone.localdate)
    done = models.BooleanField(default=False)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('habit', 'date')
        ordering = ['-date']

    def __str__(self):
        status = 'Done' if self.done else 'Pending'
        return f'{self.habit.title} - {self.date} - {status}'


class DailyReflection(models.Model):
    MOOD_CHOICES = [
        ('great', 'Great'),
        ('good', 'Good'),
        ('okay', 'Okay'),
        ('low', 'Low'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reflections')
    date = models.DateField(default=timezone.localdate)
    discipline_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text='Rate your discipline today from 1 to 10.',
    )
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, default='good')
    wins = models.TextField(blank=True, help_text='What went well today?')
    improvement = models.TextField(blank=True, help_text='What can you improve tomorrow?')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f'{self.user.username} - {self.date} - {self.discipline_score}/10'
