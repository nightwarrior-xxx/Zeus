from django.forms impor forms
from phonenumber_field.formfields import PhoneNumberField
from .models import HostDetails

class HostForm(forms.Form):
    name = forms.CharField(required=True, widget=TextInput(attrs={"placeholder": "Name"}))
    email = forms.EmailField(required=True)
    phone = forms.PhoneNumberField()

    class Meta:
        model = HostDetails
