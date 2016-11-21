from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print('yhiui')
    if created:
        print('yhiui2222')
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print('gug')
    try:
        print('gug2')
        instance.profile.save()
    except User.DoesNotExist:
        print(instance)
        Profile.objects.create(user=instance)
