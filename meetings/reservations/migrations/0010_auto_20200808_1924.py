# Generated by Django 3.1 on 2020-08-08 16:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservations', '0009_auto_20200808_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservations',
            name='employee_id',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
    ]