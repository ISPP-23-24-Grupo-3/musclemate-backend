from django.test import TestCase
from client.models import Client
from equipment.models import Equipment
from gym.models import Gym
from owner.models import Owner
from routine.models import Routine
from user.models import CustomUser
from .models import Serie,Workout
from.views import SerieListView , SerieDetailView, SerieCreateView, SerieDeleteView, SerieUpdateView
from rest_framework.test import APIRequestFactory,force_authenticate

class SerieTestCase(TestCase):
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
        self.client1 = Client.objects.create(name='Client 1', lastName='Lastname 1', email='client1@example.com',
                                              birth='2000-01-01', zipCode=12345, gender='M', phoneNumber=123456789,
                                              address='123 Test St', city='Test City', register=True, user=self.userClient,
                                              gym=self.gym)
        self.equipment = Equipment.objects.create(
            name="Mancuernas",
            brand="Marca A",
            serial_number="MNCD001",
            description="Un par de mancuernas de 5 kg cada una",
            muscular_group="arms",
            gym=self.gym
        )
        self.routine = Routine.objects.create(name="rutina pecho", client=self.client1)
        self.workout = Workout.objects.create(name='Press Banca', client=self.client1)
        self.workout.equipment.set([self.equipment])
        self.workout.routine.set([self.routine])
        self.serie = Serie.objects.create(reps= 10, weight= 100, date= '2024-03-02',duration=10.3,workout=self.workout)

    def test_serie_list_view(self):
        request = self.factory.get('/series/')
        force_authenticate(request, user=self.userClient)
        view = SerieListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_serie_detail_view(self):
        request = self.factory.get('/series/detail/')
        force_authenticate(request, user=self.userClient)
        view = SerieDetailView.as_view()
        response = view(request,pk=self.serie.pk)
        self.assertEqual(response.status_code, 200)

    def test_serie_create_view(self):
        data = {'reps': 12, 'weight': 90, 'date': '2024-03-01','duration':12.8, 'workout':self.workout.pk}
        request = self.factory.post('/series/create/',data)
        force_authenticate(request, user=self.userClient)
        view = SerieCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_serie_update_view(self):
        data = {'reps': 8, 'weight': 100, 'date': '2024-03-02','duration':12.4,'workout':self.workout.pk}
        request = self.factory.put('/series/update/',data)
        force_authenticate(request, user=self.userClient)
        view = SerieUpdateView.as_view()
        response = view(request,pk=self.serie.pk)
        self.assertEqual(response.status_code, 200)

    def test_serie_delete_view(self):
        request = self.factory.delete('/series/delete/')
        force_authenticate(request, user=self.userClient)
        view = SerieDeleteView.as_view()
        response = view(request,pk=self.serie.pk)
        self.assertEqual(response.status_code, 200)