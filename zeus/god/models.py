import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


class Profiles(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    is_active = models.BooleanField(default=False)
    phone = PhoneNumberField()

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profiles.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, *args, **kwargs):
    instance.profile.save()
