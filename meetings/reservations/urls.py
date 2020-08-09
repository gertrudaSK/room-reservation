from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index', ),
    path('profile/', views.profile, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('room/', views.select_room, name='select_room'),
    path('history/', views.reservations_list, name='all_reservations'),
    path('search/', views.search, name='search'),
    path('history/<int:id>/canceled', views.cancel_reservation, name='cancel'),
    path('create/', views.RoomCreateView.as_view(), name='create-room'),
    path('room_availability/', views.room_availability,
         name='room-availability'),
]
