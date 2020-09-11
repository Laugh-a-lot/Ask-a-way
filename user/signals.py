from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


def set_avatar(instance):
    avatar = instance.image
    gender = instance.gender
    if gender == 'Male':
        avatar = 'default.jpg'
    else:
        avatar = 'female.png'
    return avatar


def post_save_avatar(sender, instance, *args, **kwargs):
    if not instance.image:
        instance.image = set_avatar(instance)


pre_save.connect(post_save_avatar, sender=Profile)
