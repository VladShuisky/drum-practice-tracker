from time import timezone
from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.

class TrainingSession(models.Model):
    EXERCISE_CHOICES = [
        ('rudiments', 'Rudiments'),
        ('grooves', 'Grooves'),
        ('fills', 'Fills'),
        ('songs', 'Songs'),
        ('freeplay', 'Free Play'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='training_sessions')
    date = models.DateTimeField(help_text="Дата тренировки")
    duration_minutes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    exercise_type = models.CharField(max_length=50, choices=EXERCISE_CHOICES)
    notes = models.TextField(blank=True, null=True, help_text='Поле для заметок')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.exercise_type} on {self.date}"