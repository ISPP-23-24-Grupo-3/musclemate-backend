from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from gym.models import Gym
from owner.models import Owner
from user.models import CustomUser
from .models import Client
from .views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView,ClientListByGymView

class ClientTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.userClient = CustomUser.objects.create(username='test_user', email='test@example.com', rol='client')
        self.userGym = CustomUser.objects.create(username='test_user_2', email='test2@example.com', rol='gym')
        self.userOwner = CustomUser.objects.create(username='test_user_3', email='test3@example.com', rol='owner')
        self.userClient2 = CustomUser.objects.create(username='test_user_4', email='test4@example.com', rol='client')


        self.owner = Owner.objects.create(name='Owner', lastName='Owner Lastname', email='owner@example.com',
            phoneNumber=123456789, address='123 Owner St', userCustom=self.userOwner)
        self.gym = Gym.objects.create(name='Test Gym', address='123 Test St', phone_number=987654321,
            descripcion='Test Gym Description', zip_code=54321, email='gym@example.com',
            owner=self.owner, userCustom=self.userGym)
        self.client1 = Client.objects.create(name='Client 1', lastName='Lastname 1', email='client1@example.com',
            birth='2000-01-01', zipCode=12345, gender='M', phoneNumber=123456789,address='123 Test St',
            city='Test City', register=True,user=self.userClient,gym=self.gym)

    #test del list view
    def test_client_list_view_how_gym(self):
        request = self.factory.get('/clients/')
        force_authenticate(request, user=self.userGym)
        view = ClientListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_client_list_view_how_owner(self):
        request = self.factory.get('/clients/')
        force_authenticate(request, user=self.userOwner)
        view = ClientListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
    
    #test del list by gym id view
    def test_client_list__by_gymId_view_how_gym(self):
        request = self.factory.get('/clients/')
        force_authenticate(request, user=self.userGym)
        view = ClientListByGymView.as_view()
        response = view(request,gymId=self.gym.id)
        self.assertEqual(response.status_code, 200)

    def test_client_list__by_gymId_view_how_owner(self):
        request = self.factory.get('/clients/')
        force_authenticate(request, user=self.userOwner)
        view = ClientListByGymView.as_view()
        response = view(request,gymId=self.gym.id)
        self.assertEqual(response.status_code, 200)

    #test del detail view
    def test_client_detail_view_how_client(self):
        request = self.factory.get('/clients/detail/')
        force_authenticate(request, user=self.userClient)
        view = ClientDetailView.as_view()
        response = view(request, pk=self.client1.pk)
        self.assertEqual(response.status_code, 200)

    def test_client_detail_view_how_gym(self):
        request = self.factory.get('/clients/detail/')
        force_authenticate(request, user=self.userGym)
        view = ClientDetailView.as_view()
        response = view(request, pk=self.client1.pk)
        self.assertEqual(response.status_code, 200)

    def test_client_detail_view_how_owner(self):
        request = self.factory.get('/clients/detail/')
        force_authenticate(request, user=self.userOwner)
        view = ClientDetailView.as_view()
        response = view(request, pk=self.client1.pk)
        self.assertEqual(response.status_code, 200)

    #test create view
    def test_client_create_view_how_gym(self):
        data = {'name': 'New Client', 'lastName': 'New Lastname', 'email': 'newclient@example.com',
                'birth': '2000-01-01', 'zipCode': 12345, 'gender': 'O', 'phoneNumber': 123456789,
                'address': '789 Test St', 'city': 'New City', 'register': True,
                'username': 'jaime99','password': 'yourpassword','gym': self.gym.pk}
        request = self.factory.post('/clients/create/',data)
        force_authenticate(request, user=self.userGym)
        view = ClientCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_client_create_view_how_owner(self):
        data = {'name': 'New Client', 'lastName': 'New Lastname', 'email': 'newclient@example.com',
                'birth': '2000-01-01', 'zipCode': 12345, 'gender': 'O', 'phoneNumber': 123456789,
                'address': '789 Test St', 'city': 'New City', 'register': True,
                'username': 'jaime99','password': 'yourpassword','gym': self.gym.pk}
        request = self.factory.post('/clients/create/',data)
        force_authenticate(request, user=self.userOwner)
        view = ClientCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)

    #test update view
    def test_client_update_view_how_client(self):
        data = {'name': 'Updated Client', 'lastName': 'Updated Lastname', 'email': 'updatedclient@example.com',
                'birth': '2000-01-01', 'zipCode': 54321, 'gender': 'F', 'phoneNumber': 987654321,
                'address': '987 Test St', 'city': 'Updated City', 'register': False, 'user': self.userClient.pk,
                'gym': self.gym.pk}
        request = self.factory.put('/clients/update/',data)
        force_authenticate(request, user=self.userClient)
        view = ClientUpdateView.as_view()
        response = view(request, pk=self.client1.pk)
        self.assertEqual(response.status_code, 200)

    def test_client_update_view_how_gym(self):
        data = {'name': 'Updated Client', 'lastName': 'Updated Lastname', 'email': 'updatedclient@example.com',
                'birth': '2000-01-01', 'zipCode': 54321, 'gender': 'F', 'phoneNumber': 987654321,
                'address': '987 Test St', 'city': 'Updated City', 'register': False, 'user': self.userClient.pk,
                'gym': self.gym.pk}
        request = self.factory.put('/clients/update/',data)
        force_authenticate(request, user=self.userGym)
        view = ClientUpdateView.as_view()
        response = view(request, pk=self.client1.pk)
        self.assertEqual(response.status_code, 200)

    def test_client_update_view_how_owner(self):
        data = {'name': 'Updated Client', 'lastName': 'Updated Lastname', 'email': 'updatedclient@example.com',
                'birth': '2000-01-01', 'zipCode': 54321, 'gender': 'F', 'phoneNumber': 987654321,
                'address': '987 Test St', 'city': 'Updated City', 'register': False, 'user': self.userClient.pk,
                'gym': self.gym.pk}
        request = self.factory.put('/clients/update/',data)
        force_authenticate(request, user=self.userOwner)
        view = ClientUpdateView.as_view()
        response = view(request, pk=self.client1.pk)
        self.assertEqual(response.status_code, 200)

    #test delete view
    def test_client_delete_view_how_gym(self):
        request = self.factory.delete('/clients/')
        force_authenticate(request, user=self.userGym)
        view = ClientDeleteView.as_view()
        response = view(request, pk=self.client1.pk)
        self.assertEqual(response.status_code, 200)

    def test_client_delete_view_how_owner(self):
        request = self.factory.delete('/clients/')
        force_authenticate(request, user=self.userOwner)
        view = ClientDeleteView.as_view()
        response = view(request, pk=self.client1.pk)
        self.assertEqual(response.status_code, 200)