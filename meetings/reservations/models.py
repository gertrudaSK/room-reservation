from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from datetime import datetime


class Rooms(models.Model):
    title = models.CharField('Title', max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField('Image', default="default.png",
                                  upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)


class Reservations(models.Model):
    room_id = models.ForeignKey(Rooms, on_delete=models.SET_NULL, null=True,
                                db_constraint=False)
    employee_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                    db_constraint=False)
    date = models.DateField('Date', null=False, default=datetime.now,
                            blank=False)
    time_from = models.TimeField('Time From', null=False, blank=False)
    time_to = models.TimeField('Time To', null=False, blank=False)
    STATUS = (
        ('w', ('waiting')),
        ('d', ('done')),
        ('x', ('canceled')),
    )

    status = models.CharField(max_length=1,
                              choices=STATUS,
                              blank=True,
                              default='w',
                              help_text=('Status')
                              )

    def __str__(self):
        return self.room_id.title
