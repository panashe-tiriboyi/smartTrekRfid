from django.urls import path, include
from .views import HomeAttendance
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.HomeAttendance, name='homeAttendance'),
    path('signup/', views.signup, name='signup'),
    path('checkIn/', views.checkIn, name='checkIn'),
    path('checkOut/', views.checkOut, name='checkOut'),
    path('success/', views.success, name='success'),
    path('error/', views.error, name='error'),
    path('accounts/', include('django.contrib.auth.urls')),
    
]






