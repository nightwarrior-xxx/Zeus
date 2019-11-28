from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField

class Host(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField()
    phone = PhoneNumberField(region="IN")
    address = models.CharField(max_length=250)

    def __str__(self):
        return self.user.username


class Clients(models.Model):
    name = models.CharField(max_length=250)
    phone = PhoneNumberField()
    checkInTime = models.DateTimeField(auto_now_add=True)
    checkOutTime = models.DateTimeField(auto_now=True)
    email = models.EmailField()
    inMeeting = models.BooleanField(default=True)

    def __str__(self):
        return self.name
