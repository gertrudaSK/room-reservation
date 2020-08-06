from django.apps import AppConfig


class ReservationsConfig(AppConfig):
    name = 'reservations'

    def ready(self):
        from .signals import create_profile, save_profile
