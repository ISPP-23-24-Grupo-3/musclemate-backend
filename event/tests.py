from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from client.models import Client
from gym.models import Gym
from owner.models import Owner
from user.models import CustomUser
from .models import Event
from .views import EventListView, EventListByGymView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView
from datetime import timedelta

class EventAPITestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.userOwner = CustomUser.objects.create(username='test_user', email='test@example.com', rol='owner')
        self.userGym = CustomUser.objects.create(username='test_user2', email='test2@example.com', rol='gym')
        self.userClient = CustomUser.objects.create(username='test_user_3', email='test3@example.com', rol='client')

        self.owner = Owner.objects.create(name='Owner', last_name='Owner last_name', email='owner@example.com',
                                           phone_number=123456789, address='123 Owner St', userCustom=self.userOwner)
        self.gym = Gym.objects.create(name='Test Gym', address='123 Test St', phone_number=987654321,
                                       descripcion='Test Gym Description', zip_code=54321, email='gym@example.com',
                                       owner=self.owner, userCustom=self.userGym)
        self.client = Client.objects.create(name='Client 1', last_name='last_name 1', email='client1@example.com',
                                              birth='2000-01-01', zipCode=12345, gender='M', phone_number=123456789,
                                              address='123 Test St', city='Test City', register=True, user=self.userClient,
                                              gym=self.gym)
        self.event1 = Event.objects.create(name='Event 1',description='This is event 1',capacity=50,
                                           attendees=25, instructor='John Doe',
                                           date='2024-03-01',isClickable=True,duration=timedelta(hours=1),intensity='M',
                                           isNotice=False,gym=self.gym)
    #tests del list view
    def test_event_list_view_how_owner(self):
        request = self.factory.get('/events/')
        force_authenticate(request, user=self.userOwner)
        view = EventListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_event_list_view_how_gym(self):
        request = self.factory.get('/events/')
        force_authenticate(request, user=self.userGym)
        view = EventListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)


    #tests del list view by gym id
    def test_event_list_by_gym_view_how_gym(self):
        request = self.factory.get('/events/gym/')
        force_authenticate(request, user=self.userGym)
        view = EventListByGymView.as_view()
        response = view(request,gymId=self.gym.pk)
        self.assertEqual(response.status_code, 200)

    def test_event_list_by_gym_view_how_owner(self):
        request = self.factory.get('/events/gym/')
        force_authenticate(request, user=self.userOwner)
        view = EventListByGymView.as_view()
        response = view(request,gymId=self.gym.pk)
        self.assertEqual(response.status_code, 200)

    def test_event_list_by_gym_view_how_client(self):
        request = self.factory.get('/events/gym/')
        force_authenticate(request, user=self.userClient)
        view = EventListByGymView.as_view()
        response = view(request,gymId=self.gym.pk)
        self.assertEqual(response.status_code, 200)


    #tests del detail view
    def test_event_detail_view_how_gym(self):
        request = self.factory.get('/events/')
        force_authenticate(request, user=self.userGym)
        view = EventDetailView.as_view()
        response = view(request, pk=self.event1.pk)
        self.assertEqual(response.status_code, 200)

    def test_event_detail_view_how_owner(self):
        request = self.factory.get('/events/')
        force_authenticate(request, user=self.userOwner)
        view = EventDetailView.as_view()
        response = view(request, pk=self.event1.pk)
        self.assertEqual(response.status_code, 200)

    def test_event_detail_view_how_client(self):
        request = self.factory.get('/events/')
        force_authenticate(request, user=self.userClient)
        view = EventDetailView.as_view()
        response = view(request, pk=self.event1.pk)
        self.assertEqual(response.status_code, 200)

    #tests del create view
    def test_event_create_view_how_gym(self):
        data = {'name':'Event 3','description':'This is event 3','capacity':30,
                'attendees':15 , 'instructor':'Jane Smith',
                'date':'2024-03-02','isClickable':True,'duration':timedelta(hours=1),'intensity':'H',
                'isNotice':True,'gym':self.gym.pk}
        request = self.factory.post('/events/create/', data)
        force_authenticate(request, user=self.userGym)
        view = EventCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_event_create_view_name_validator(self):
        data = {'name':2,'description':'This is event 3','capacity':30,
                'attendees':15 , 'instructor':'Jane Smith',
                'date':'2024-03-02','isClickable':True,'duration':timedelta(hours=1),'intensity':'H',
                'isNotice':True,'gym':self.gym.pk}
        request = self.factory.post('/events/create/', data)
        force_authenticate(request, user=self.userGym)
        view = EventCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('El nombre debe contener letras.',response.data['name'][0])

    def test_event_create_view_description_validator(self):
        data = {'name':'event','description':5,'capacity':30,
                'attendees':15 , 'instructor':'Jane Smith',
                'date':'2024-03-02','isClickable':True,'duration':timedelta(hours=1),'intensity':'H',
                'isNotice':True,'gym':self.gym.pk}
        request = self.factory.post('/events/create/', data)
        force_authenticate(request, user=self.userGym)
        view = EventCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('La descripción debe contener letras.',response.data['description'][0])

    def test_event_create_view_how_owner(self):
        data = {'name':'Event 3','description':'This is event 3','capacity':30,
                'attendees':15 , 'instructor':'Jane Smith',
                'date':'2024-03-02','isClickable':True,'duration':timedelta(hours=1),'intensity':'H',
                'isNotice':True,'gym':self.gym.pk}
        request = self.factory.post('/events/create/', data)
        force_authenticate(request, user=self.userOwner)
        view = EventCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)


    #tests del update view
    def test_event_update_view_how_gym(self):
        data = {'name':'Event 4','description':'This is event 4','capacity':30,
                'attendees':15, 'instructor':'Jane Smith',
                'date':'2024-03-02','isClickable':True,'duration':timedelta(hours=1.5),'intensity':'H',
                'isNotice':True,'gym':self.gym.pk}
        request = self.factory.put('/events/update/', data)
        force_authenticate(request, user=self.userGym)
        view = EventUpdateView.as_view()
        response = view(request, pk=self.event1.pk)
        self.assertEqual(response.status_code, 200)

    def test_event_update_view_how_owner(self):
        data = {'name':'Event 4','description':'This is event 4','capacity':30,
                'attendees':15, 'instructor':'Jane Smith',
                'date':'2024-03-02','isClickable':True,'duration':timedelta(hours=1.5),'intensity':'H',
                'isNotice':True,'gym':self.gym.pk}
        request = self.factory.put('/events/update/', data)
        force_authenticate(request, user=self.userOwner)
        view = EventUpdateView.as_view()
        response = view(request, pk=self.event1.pk)
        self.assertEqual(response.status_code, 200)


    #tests del delete view
    def test_event_delete_view_how_gym(self):
        request = self.factory.delete('/events/')
        force_authenticate(request, user=self.userGym)
        view = EventDeleteView.as_view()
        response = view(request, pk=self.event1.pk)
        self.assertEqual(response.status_code, 200)

    def test_event_delete_view_how_owner(self):
        request = self.factory.delete('/events/')
        force_authenticate(request, user=self.userOwner)
        view = EventDeleteView.as_view()
        response = view(request, pk=self.event1.pk)
        self.assertEqual(response.status_code, 200)