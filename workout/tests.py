from django.test import TestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from .views import (WorkoutListView, WorkoutDetailView, WorkoutCreateView,
    WorkoutUpdateView, WorkoutDeleteView,WorkoutListByClientListView,
    WorkoutListByRoutineListView,WorkoutListByEquipmentListView)
from .models import Workout, Client, Equipment, Routine
from gym.models import Gym
from user.models import CustomUser
from owner.models import Owner

class WorkoutTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create(username='testuser', email='test@example.com', rol='client', password='testpassword', id=123456)
        self.user1 = CustomUser.objects.create(username='testuser1', email='test1@example.com', rol='owner')
        self.user2 = CustomUser.objects.create(username='testuser2', email='test2@example.com', rol='gym')
        self.user3 = CustomUser.objects.create(username='testuser3', email='test3@example.com', rol='gym')

        self.owner = Owner.objects.create(
            name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone_number=123456789,
            address='123 Owner St',
            userCustom=self.user1
        )
        self.gym = Gym.objects.create(
            name='Test Gym',
            address='123 Test St',
            phone_number=123456789,
            descripcion='Test Description',
            zip_code=12345,
            email='test@example.com',
            owner=Owner.objects.get(name=self.owner.name),
            userCustom=CustomUser.objects.get(pk=self.user2.pk)
        )
        self.gym2 = Gym.objects.create(
            name='Test Gym',
            address='123 Test St',
            phone_number=123456789,
            descripcion='Test Description',
            zip_code=12345,
            email='test@example.com',
            owner=Owner.objects.get(name=self.owner.name),
            userCustom=CustomUser.objects.get(pk=self.user3.pk)
        )
        self.client = Client.objects.create(
            user=self.user,
            gym=self.gym,
            name='test',
            last_name='user',
            email='test@gmail.com',
            zipCode=12345,
            phone_number=1234567890,
            address='1234 Test St',
            city='Test City',
            register=True
        )
        self.client2 = Client.objects.create(
            user=self.user1,
            gym=self.gym,
            name='test2',
            last_name='user2',
            email='test3@gmail.com0',
            zipCode=12345,
            phone_number=1234567890,
            address='1234 Test St',
            city='Test City',
            register=True
        )
        self.equipment = Equipment.objects.create(name='test', gym=self.gym2 )
        self.routine = Routine.objects.create(name='test', client=self.client2)
        self.workout = Workout.objects.create(name='test',client=self.client)
        self.workout.equipment.set([self.equipment])
        self.workout.routine.set([self.routine])
        self.workout2 = Workout.objects.create(name='test2',client=self.client2)

    def test_workout_list_view_authenticated_user(self):
        request = self.factory.get('/workouts/')
        force_authenticate(request, user=self.user)
        view = WorkoutListView.as_view()
        response = view(request)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_workout_list_view_superuser(self):
        request = self.factory.get('/workouts/')
        self.user.is_superuser = True
        force_authenticate(request, user=self.user)
        response = WorkoutListView.as_view()(request)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, 200)

    def test_workout_list_by_equipment_view_client(self):
        request = self.factory.get('/workouts/byEquipment/{self.equipment.id}')
        force_authenticate(request, user=self.user)
        view = WorkoutListByEquipmentListView.as_view()
        response = view(request,equipmentId=self.equipment.id)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_workout_list_by_routine_view_client(self):
        request = self.factory.get('/workouts/byRoutine/{self.routine.id}')
        force_authenticate(request, user=self.user)
        view = WorkoutListByRoutineListView.as_view()
        response = view(request,routineId=self.routine.id)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_workout_list_by_client_view_owner(self):
        request = self.factory.get('/workouts/byClient/{self.client.id}')
        force_authenticate(request, user=self.user1)
        view = WorkoutListByClientListView.as_view()
        response = view(request,clientId=self.client.id)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_workout_list_by_client_view_gym(self):
        request = self.factory.get('/workouts/byClient/{self.client.id}')
        force_authenticate(request, user=self.user2)
        view = WorkoutListByClientListView.as_view()
        response = view(request,clientId=self.client.id)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_workout_detail_view(self):
        request = self.factory.get('/workouts/detail/{self.workout.id}')
        force_authenticate(request, user=self.user)
        response = WorkoutDetailView.as_view()(request, pk=self.workout.pk)
        self.assertEqual(response.data.get('client_id'), self.client.id)
        self.assertEqual(response.status_code, 200)

    def test_workout_create_view(self):
        request = self.factory.post('/workouts/create/', data = {'name': 'test3', 'client': self.client.id})
        force_authenticate(request, user=self.user)
        response = WorkoutCreateView.as_view()(request)
        self.assertTrue(Workout.objects.filter(name='test3').exists())
        self.assertEqual(response.status_code, 201)

    def test_workout_update_view(self):
        request = self.factory.put('/workouts/update/{self.workout.id}/', data = {'name': 'test4', 'client': self.client.id})
        force_authenticate(request, user=self.user)
        response = WorkoutUpdateView.as_view()(request, pk=self.workout.pk)
        self.assertTrue(Workout.objects.filter(name='test4').exists())
        self.assertFalse(Workout.objects.filter(name='test3').exists())
        self.assertEqual(response.status_code, 200)

    def test_workout_delete_view(self):
        request = self.factory.delete('/workouts/delete/{self.workout.id}/')
        force_authenticate(request, user=self.user)
        response = WorkoutDeleteView.as_view()(request, pk=self.workout.pk)
        self.assertFalse(Workout.objects.filter(name='test3').exists())
        self.assertEqual(response.status_code, 200)

    def test_negative_workout_detail_view_unauthorized(self):
        request = self.factory.get('/workouts/detail/{self.workout.id}/')
        request.user = self.user2
        response = WorkoutDetailView.as_view()(request, pk=self.workout.pk)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'You are not allowed to see this workout')

    def test_negative_workout_create_view_invalid_equipment(self):
        request = self.factory.post('/workouts/create/', data={'name': 'test3', 'client': self.client.id,
            'equipment': [self.equipment.id]})
        force_authenticate(request, user=self.user)
        response = WorkoutCreateView.as_view()(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'],
            'You are not allowed to create a workout with this equipment or routine')

    def test_negative_workout_create_view_invalid_routine(self):
        request = self.factory.post('/workouts/', data={'name': 'test3', 'client': self.client.id,
            'routine': [self.routine.id]})
        force_authenticate(request, user=self.user)
        response = WorkoutCreateView.as_view()(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'],
            'You are not allowed to create a workout with this equipment or routine')

    def test_negative_workout_update_view_unauthorized(self):
        request = self.factory.put('/workouts/update/{self.workout.id}/', data={'name': 'test4', 'client': self.client.id})
        force_authenticate(request, user=self.user2)
        response = WorkoutUpdateView.as_view()(request, pk=self.workout.pk)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'You are not allowed to update this workout')

    def test_negative_workout_delete_view_unauthorized(self):
        request = self.factory.delete('/workouts/delete/{self.workout.id}')
        request.user = self.user2
        force_authenticate(request, user=request.user)
        response = WorkoutDeleteView.as_view()(request, pk=self.workout.pk)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'You are not allowed to delete this workout')