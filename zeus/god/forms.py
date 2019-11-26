from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class HostLogin(forms.Form):

    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={"class": "input-details", "placeholder": "Username"}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={"class": "input-details", "placeholder": "Password"}))


class HostSignup(UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput())
    last_name = forms.CharField(required=False, widget=forms.TextInput())
    email = forms.EmailField(required=True)
    phone = PhoneNumberField(required=True, region='IN')
    username = forms.CharField(required=True, max_length=250)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, widget=forms.PasswordInput())


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username','email', 'phone', 'password1', 'password2')


    def save(self, commit=True):
        user = super(HostSignup, self).save(commit=False)
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']
        user.email=self.cleaned_data['email']
        user.profile.phone=self.cleaned_data['phone']
        user.username=self.cleaned_data['username']
       
        if commit:

            user.save()
        
        return user

