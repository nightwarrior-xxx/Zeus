from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# model for host detail
class HostDetails(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = PhoneNumberField()


# model for client detail
class ClientDetails(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = PhoneNumberField()
    checkInTime = models.TimeField(auto_now_add=True)
    checkOutTime = models.TimeField()
