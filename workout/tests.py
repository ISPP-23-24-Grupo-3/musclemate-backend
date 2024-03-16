from django.test import TestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from .views import WorkoutListView, WorkoutDetailView, WorkoutCreateView, WorkoutUpdateView, WorkoutDeleteView
from .models import Workout, Client, Equipment, Routine
from gym.models import Gym
from user.models import CustomUser
from owner.models import Owner

class WorkoutTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.user = CustomUser.objects.create(username='testuser', email='test@example.com', rol='client', password='testpassword', id=123456)
        cls.user1 = CustomUser.objects.create(username='testuser1', email='test1@example.com', rol='owner')
        cls.user2 = CustomUser.objects.create(username='testuser2', email='test2@example.com', rol='gym')
        cls.user3 = CustomUser.objects.create(username='testuser3', email='test3@example.com', rol='gym')

        cls.owner = Owner.objects.create(
            name='John',
            lastName='Doe',
            email='john.doe@example.com',
            phoneNumber=123456789,
            address='123 Owner St',
            userCustom=cls.user1
        )
        cls.gym = Gym.objects.create(
            name='Test Gym',
            address='123 Test St',
            phone_number=123456789,
            descripcion='Test Description',
            zip_code=12345,
            email='test@example.com',
            owner=Owner.objects.get(name=cls.owner.name),
            userCustom=CustomUser.objects.get(pk=cls.user2.pk)
        )
        cls.gym2 = Gym.objects.create(
            name='Test Gym',
            address='123 Test St',
            phone_number=123456789,
            descripcion='Test Description',
            zip_code=12345,
            email='test@example.com',
            owner=Owner.objects.get(name=cls.owner.name),
            userCustom=CustomUser.objects.get(pk=cls.user3.pk)
        )
        cls.client = Client.objects.create(
            user=cls.user,
            gym=cls.gym,
            name='test',
            lastName='user',
            email='test@gmail.com',
            zipCode=12345,
            phoneNumber=1234567890,
            address='1234 Test St',
            city='Test City',
            register=True
        )
        cls.client2 = Client.objects.create(
            user=cls.user1,
            gym=cls.gym,
            name='test2',
            lastName='user2',
            email='test3@gmail.com0',
            zipCode=12345,
            phoneNumber=1234567890,
            address='1234 Test St',
            city='Test City',
            register=True
        )
        cls.workout = Workout.objects.create(name='test',client=cls.client)
        cls.workout2 = Workout.objects.create(name='test2',client=cls.client2)
        cls.equipment = Equipment.objects.create(name='test', gym=cls.gym2 )
        cls.routine = Routine.objects.create(name='test', client=cls.client2)

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

    def test_workout_detail_view(self):
        request = self.factory.get('/workouts/detail/{self.workout.id}')
        client = Client.objects.get(user=self.user)
        force_authenticate(request, user=self.user)
        response = WorkoutDetailView.as_view()(request, pk=self.workout.pk)
        self.assertEqual(response.data.get('client_id'), client.id)
        self.assertEqual(response.status_code, 200)

    def test_workout_create_view(self):
        client = Client.objects.get(user=self.user)
        request = self.factory.post('/workouts/create/', data = {'name': 'test3', 'client': client.id})
        force_authenticate(request, user=self.user)
        response = WorkoutCreateView.as_view()(request)
        self.assertTrue(Workout.objects.filter(name='test3').exists())
        self.assertEqual(response.status_code, 201)

    def test_workout_update_view(self):
        client = Client.objects.get(user=self.user)
        request = self.factory.put('/workouts/update/{self.workout.id}/', data = {'name': 'test4', 'client': client.id})
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
        client = Client.objects.get(user=self.user)
        request = self.factory.post('/workouts/create/', data={'name': 'test3', 'client': client.id, 'equipment': [self.equipment.id]})
        force_authenticate(request, user=self.user)
        response = WorkoutCreateView.as_view()(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'You are not allowed to create a workout with this equipment or routine')
    
    def test_negative_workout_create_view_invalid_routine(self):
        client = Client.objects.get(user=self.user)
        request = self.factory.post('/workouts/', data={'name': 'test3', 'client': client.id, 'routine': [self.routine.id]})
        force_authenticate(request, user=self.user)
        response = WorkoutCreateView.as_view()(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'You are not allowed to create a workout with this equipment or routine')
    
    def test_negative_workout_update_view_unauthorized(self):
        client = Client.objects.get(user=self.user)
        request = self.factory.put('/workouts/update/{self.workout.id}/', data={'name': 'test4', 'client': client.id})
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
