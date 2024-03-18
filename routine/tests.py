from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from gym.models import Gym
from owner.models import Owner
from user.models import CustomUser
from .models import Routine,Client
from .views import RoutineCreateView,RoutineDeleteView,RoutineDetailView,RoutineListView,RoutineUpdateView

class ClientTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.userClient = CustomUser.objects.create(username='test_user', email='test@example.com', rol='client')
        self.userGym = CustomUser.objects.create(username='test_user_2', email='test2@example.com', rol='gym')
        self.userOwner = CustomUser.objects.create(username='test_user_3', email='test3@example.com', rol='owner')

        self.owner = Owner.objects.create(name='Owner', lastName='Owner Lastname', email='owner@example.com',
            phoneNumber=123456789, address='123 Owner St', userCustom=self.userOwner)
        self.gym = Gym.objects.create(name='Test Gym', address='123 Test St', phone_number=987654321,
            descripcion='Test Gym Description', zip_code=54321, email='gym@example.com',
            owner=self.owner, userCustom=self.userGym)
        self.client = Client.objects.create(name='Client 1', lastName='Lastname 1', email='client1@example.com',
            birth='2000-01-01', zipCode=12345, gender='M', phoneNumber=123456789,address='123 Test St',
            city='Test City', register=True,user=self.userClient,gym=self.gym)
        self.routine=Routine.objects.create(name= 'rutina pecho',client= self.client)

    #test del list view
    def test_routine_list_view_how_client(self):
        request = self.factory.get('/routines/')
        force_authenticate(request, user=self.userClient)
        view = RoutineListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)


    #test del detail view
    def test_routine_detail_view_how_client(self):
        request = self.factory.get('/routines/detail/')
        force_authenticate(request, user=self.userClient)
        view = RoutineDetailView.as_view()
        response = view(request, pk=self.routine.pk)
        self.assertEqual(response.status_code, 200)


    #test create view
    def test_routine_create_view_how_client(self):
        data = {'name': 'New Routine', 'client':self.client.pk}
        request = self.factory.post('/routines/create/',data)
        force_authenticate(request, user=self.userClient)
        view = RoutineCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)


    #test update view
    def test_routine_update_view_how_client(self):
        data = {'name': 'Updated Routine', 'client':self.client.pk}
        request = self.factory.put('/routines/update/',data)
        force_authenticate(request, user=self.userClient)
        view = RoutineUpdateView.as_view()
        response = view(request, pk=self.routine.pk)
        self.assertEqual(response.status_code, 200)


    #test delete view
    def test_routine_delete_view_how_client(self):
        request = self.factory.delete('/routines/')
        force_authenticate(request, user=self.userClient)
        view = RoutineDeleteView.as_view()
        response = view(request, pk=self.routine.pk)
        self.assertEqual(response.status_code, 204)