
from django.contrib import admin
from django.urls import path, include
from god.views import (
    home,
    hostSignup,
    hostLogin
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('hostLogin/', hostLogin, name='hostLogin'),
    path('hostSignup/', hostSignup, name='hostSignup'),
]
