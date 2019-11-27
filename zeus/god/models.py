from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField

class Host(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField()
    phone = PhoneNumberField(region="IN")
    address = models.CharField(max_length=250)

    def __str__(self):
        return self.user.username
