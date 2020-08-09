from django.contrib import admin
from .models import Rooms, Profile, Reservations


class RoomsAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ReservationsAdmin(admin.ModelAdmin):
    list_display = (
                    'room_id', 'employee_id', 'date', 'time_from', 'time_to',
                    'status')


admin.site.register(Rooms, RoomsAdmin)
admin.site.register(Profile)
admin.site.register(Reservations, ReservationsAdmin)
