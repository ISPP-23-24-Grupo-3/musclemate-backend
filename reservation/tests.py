from datetime import timedelta
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from gym.models import Gym
from owner.models import Owner
from event.models import Event

from user.models import CustomUser
from .models import Reservation
from client.models import Client
from .views import ReservationListView, ReservationListByClientView, ReservationDetailView, ReservationCreateView, ReservationUpdateView, ReservationDeleteView

class ReservationTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create(username='test_user', email='test@example.com', rol='owner')
        self.user2 = CustomUser.objects.create(username='test_user2', email='test2@example.com', rol='client')
        self.user3 = CustomUser.objects.create(username='test_user3', email='test3@example.com', rol='gym')
        self.owner = Owner.objects.create(name='Owner', lastName='Owner Lastname', email='owner@example.com',
                                           phoneNumber=123456789, address='123 Owner St', userCustom=self.user)
        self.gym = Gym.objects.create(name='Test Gym', address='123 Test St', phone_number=987654321,
                                       descripcion='Test Gym Description', zip_code=54321, email='gym@example.com',
                                       owner=self.owner, userCustom=self.user3)
        self.event1 = Event.objects.create(name='Event 1',description='This is event 1',capacity=50,instructor='John Doe',
                                           date='2024-03-01',isClickable=True,duration=timedelta(hours=1),intensity='M',
                                           isNotice=False,gym=self.gym)
        self.event2 = Event.objects.create(name='Event 2',description='This is event 2',capacity=50,instructor='John Doe',
                                           date='2024-03-01',isClickable=True,duration=timedelta(hours=1.5),intensity='M',
                                           isNotice=False,gym=self.gym)
        self.client1 = Client.objects.create(id=758168,name='Client 1', lastName='Lastname 1', email='client1@example.com',
                                              birth='2000-01-01', zipCode=12345, gender='M', phoneNumber=123456789,
                                              address='123 Test St', city='Test City', register=True, user=self.user2,
                                              gym=self.gym)

        self.reservation = Reservation.objects.create(client=self.client1, event=self.event1)

    def test_reservation_list_view(self):
        request = self.factory.get('/reservations/all/')
        view = ReservationListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_reservation_list_by_client_view(self):
        request = self.factory.get('/reservations/')
        request.user = self.user2
        view = ReservationListByClientView.as_view()
        response = view(request,clientId=self.client1.pk)
        self.assertEqual(response.status_code, 200)

    def test_reservation_detail_view(self):
        request = self.factory.get('/reservations/')
        view = ReservationDetailView.as_view()
        response = view(request, pk=self.reservation.pk)
        self.assertEqual(response.status_code, 200)

    def test_reservation_create_view(self):
        data = {'client':self.client1.pk, 'event':self.event2.pk}
        request = self.factory.post('/reservations/create/', data=data)
        view = ReservationCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_reservation_update_view(self):
        data = {'client':self.client1.pk, 'event':self.event2.pk}
        request = self.factory.post('/reservations/update/', data=data)
        view = ReservationUpdateView.as_view()
        response = view(request, pk=self.reservation.pk)
        self.assertEqual(response.status_code, 200)

    def test_reservation_delete_view(self):
        request = self.factory.delete('/reservations/')
        view = ReservationDeleteView.as_view()
        response = view(request, pk=self.reservation.pk)
        self.assertEqual(response.status_code, 200)
