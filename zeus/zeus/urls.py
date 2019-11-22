
from django.contrib import admin
from django.urls import path, include
from god.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('host/', include('god.urls', namespace='host'))
]
