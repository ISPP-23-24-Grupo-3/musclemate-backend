from django.test import TestCase
from rest_framework.test import APIRequestFactory
from gym.models import Gym
from owner.models import Owner

from user.models import CustomUser
from .models import Client
from .views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView

class ClientTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create(username='test_user', email='test@example.com', rol='client')
        self.user2 = CustomUser.objects.create(username='test_user_2', email='test2@example.com', rol='gym')
        self.user3 = CustomUser.objects.create(username='test_user_3', email='test3@example.com', rol='owner')
        self.user4 = CustomUser.objects.create(username='test_user_4', email='test4@example.com', rol='client')


        self.owner = Owner.objects.create(name='Owner', lastName='Owner Lastname', email='owner@example.com',
                                           phoneNumber=123456789, address='123 Owner St', userCustom=self.user3)
        self.gym = Gym.objects.create(name='Test Gym', address='123 Test St', phone_number=987654321,
                                       descripcion='Test Gym Description', zip_code=54321, email='gym@example.com',
                                       owner=self.owner, userCustom=self.user2)
        self.client1 = Client.objects.create(name='Client 1', lastName='Lastname 1', email='client1@example.com',
                                              birth='2000-01-01', zipCode=12345, gender='M', phoneNumber=123456789,
                                              address='123 Test St', city='Test City', register=True, user=self.user,
                                              gym=self.gym)

    def test_client_list_view(self):
        request = self.factory.get('/clients/')
        view = ClientListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_client_detail_view(self):
        request = self.factory.get('/clients/')
        view = ClientDetailView.as_view()
        response = view(request, pk=self.client1.pk)
        self.assertEqual(response.status_code, 200)

    def test_client_create_view(self):
        data = {'name': 'New Client', 'lastName': 'New Lastname', 'email': 'newclient@example.com',
                'birth': '2000-01-01', 'zipCode': 12345, 'gender': 'O', 'phoneNumber': 123456789,
                'address': '789 Test St', 'city': 'New City', 'register': True, 'user': self.user4.pk,
                'gym': self.gym.pk}
        request = self.factory.post('/clients/create/',data)
        view = ClientCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_client_update_view(self):
        data = {'name': 'Updated Client', 'lastName': 'Updated Lastname', 'email': 'updatedclient@example.com',
                'birth': '2000-01-01', 'zipCode': 54321, 'gender': 'F', 'phoneNumber': 987654321,
                'address': '987 Test St', 'city': 'Updated City', 'register': False, 'user': self.user.pk,
                'gym': self.gym.pk}
        request = self.factory.post('/clients/update/',data)
        view = ClientUpdateView.as_view()
        response = view(request, pk=self.client1.pk)
        self.assertEqual(response.status_code, 200)

    def test_client_delete_view(self):
        request = self.factory.delete('/clients/')
        view = ClientDeleteView.as_view()
        response = view(request, pk=self.client1.pk)
        self.assertEqual(response.status_code, 200)
