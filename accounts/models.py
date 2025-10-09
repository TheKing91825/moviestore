from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    REGION_CHOICES = [
        ('northeast', 'Northeast'),
        ('southeast', 'Southeast'),
        ('midwest', 'Midwest'),
        ('southwest', 'Southwest'),
        ('west', 'West'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    region = models.CharField(max_length=20, choices=REGION_CHOICES, default='northeast')
    
    def __str__(self):
        return f"{self.user.username} - {self.get_region_display()}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a User is created"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
