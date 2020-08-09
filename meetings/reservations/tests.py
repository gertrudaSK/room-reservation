from django.test import TestCase
from .forms import RoomCreateForm
from .models import Rooms, Reservations
from django.urls import reverse
from .views import RoomCreateView
from django.contrib.auth.models import User


class RoomCreateViewTest(TestCase):
    def setUp(self):
        self.view = RoomCreateView()

    def test_attrs(self):
        self.assertEqual(self.view.model, Rooms)
        self.assertEqual(self.view.form_class, RoomCreateForm)
        self.assertEqual(self.view.success_url, "/reservations/")
        self.assertEqual(self.view.template_name, 'room_CreateView.html')
        self.assertEqual(self.view.success_message,
                         "The meeting room was successfully created!")


class TestModels(TestCase):
    def test_reservations_has_title(self):
        test_room = Rooms.objects.create(id=1, title="Test Room")
        employee = User.objects.create(id=101, username='NameTest',
                                       email='test@test.com',
                                       first_name="Test Test")
        reservation = Reservations.objects.create(room_id=test_room,
                                                  employee_id=employee,
                                                  date='2020-12-31',
                                                  time_from='09:00:00',
                                                  time_to='10:00:00',
                                                  status='w')
        self.assertEqual(str(reservation), 'Test Room')


class TestReservationsView(TestCase):
    def test_anonymous_cannot_see_page(self):
        response = self.client.get(reverse("all_reservations"))
        self.assertRedirects(response,
                             '/reservations/?next=/reservations/history/')
