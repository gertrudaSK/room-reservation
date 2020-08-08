from django.contrib import admin
from .models import Rooms, Profile, Reservations

class RoomsAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Rooms, RoomsAdmin)
admin.site.register(Profile)
admin.site.register(Reservations)

