from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PomodoroSession(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=25)
    session_name = models.CharField(max_length=200, default="جلسه مطالعه")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_paused = models.BooleanField(default=False)
    paused_at = models.DateTimeField(null=True, blank=True)
    total_paused_duration = models.DurationField(default=timezone.timedelta(0))

    class Meta:
        ordering = ["-start_time"]

    def __str__(self):
        return f"{self.session_name} - {self.duration_minutes}min ({'Active' if self.is_active else 'Completed'})"

    @property
    def elapsed_time(self):
        if not self.is_active and self.end_time:
            return self.end_time - self.start_time - self.total_paused_duration

        now = timezone.now()
        if self.is_paused and self.paused_at:
            return self.paused_at - self.start_time - self.total_paused_duration

        return now - self.start_time - self.total_paused_duration

    @property
    def remaining_time(self):
        total_duration = timezone.timedelta(minutes=self.duration_minutes)
        elapsed = self.elapsed_time
        remaining = total_duration - elapsed
        return max(remaining, timezone.timedelta(0))


class PomodoroLog(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_name = models.CharField(max_length=200)
    duration_minutes = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    completed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.session_name} - {self.duration_minutes}min ({self.start_time.strftime('%Y-%m-%d %H:%M')})"
