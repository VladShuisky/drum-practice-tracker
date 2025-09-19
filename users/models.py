from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.username


class Stats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="stats")
    total_sessions = models.IntegerField(default=0)
    total_minutes = models.IntegerField(default=0)
    avg_duration = models.FloatField(default=0.0)
    streak_days = models.IntegerField(default=0)
    last_calculated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stats for {self.user.username}"