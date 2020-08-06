from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from datetime import datetime


class Employee(models.Model):
    name = models.CharField('Name', max_length=200)
    email = models.CharField('email', max_length=200)

    def __str__(self):
        return self.name


class Rooms(models.Model):
    name = models.CharField('Name', max_length=200)
    STATUS = (
        ('a', 'available'),
        ('u', 'unavailable'),
    )

    status = models.CharField(max_length=1,
                              choices=STATUS,
                              default='a'
                              )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField('Image', default="default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)

class Reservations(models.Model):
    room_id = models.ForeignKey(Rooms, on_delete=models.SET_NULL, null=False, db_constraint=False)
    employee_id =
    date = models.DateField('Date', null=False, default=datetime.now, blank=False)
    time_from = models.TimeField('Time From', null=False, default=datetime.now, blank=False)
    time_due =

