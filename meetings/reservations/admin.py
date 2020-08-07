from django.contrib import admin
from .models import Rooms, Employee, Profile, Reservations

class RoomsAdmin(admin.ModelAdmin):
    list_display = ('title',)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

admin.site.register(Rooms, RoomsAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Profile)
admin.site.register(Reservations)

