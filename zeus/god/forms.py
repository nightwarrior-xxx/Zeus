from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import HostDetails


class HostForm(forms.ModelForm):
    
    class Meta:
        model = HostDetails
        fields = ['name', 'email', 'phone']


    def clean_email(self):
        email = self.cleaned_data('email')
        user_email = HostDetails(email=email)
        if user_email.exists():
            return forms.ValidationError("Email already exists")

    def clean_hone(self):
        phone = self.cleaned_data('phone')
        user_phone = HostDetails(phone=phone)
        if user_phone.exists():
            return forms.ValidationError("Phone number already registered")
    