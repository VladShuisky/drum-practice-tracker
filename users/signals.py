from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Stats

@receiver(post_save, sender=User)
def create_user_stats(sender, instance, created, **kwargs):
    if created:
        Stats.objects.create(user=instance)