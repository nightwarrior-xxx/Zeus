
from django.urls import path
from .views import host_login

app_name = 'host'

urlpatterns = [
    path('', host_login, name='host_login'),
]