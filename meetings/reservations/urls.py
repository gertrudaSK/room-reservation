from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index',),
    path('profile/', views.profile, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('room/', views.select_room, name='select_room'),
]