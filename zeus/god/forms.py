from django import forms
from .models import Host
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class HostSignUp(UserCreationForm):
    email = forms.EmailField()
    phone = PhoneNumberField()
    address = forms.CharField()
    password1 = forms.CharField(widget = forms.PasswordInput())
    password2 = forms.CharField(widget = forms.PasswordInput())


    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2', 'address']

    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email)
        if user.exists():
            return forms.ValidationError('Email already taken')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        user = Host.objects.filter(phone=phone)
        if user.exists():
            return forms.ValidationError('Phone number alredy exists')
        return phone
    
    def clean(self):
        data = self.cleaned_data
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1!=password2:
            return forms.ValidationError('Password not match')
        return data
