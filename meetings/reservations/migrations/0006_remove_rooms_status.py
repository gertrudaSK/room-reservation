# Generated by Django 3.1 on 2020-08-06 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0005_auto_20200806_1340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rooms',
            name='status',
        ),
    ]
