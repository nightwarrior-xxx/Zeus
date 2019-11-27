from django.urls import path
from .views import clientRegister, ClientCheckout


app_name = 'god'

urlpatterns = [
    path('', clientRegister, name='client'),
    path('clientCheckout/', ClientCheckout, name='checkout')
]
