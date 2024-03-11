from django.test import TestCase
from rest_framework.test import APIRequestFactory
from gym.models import Gym
from owner.models import Owner
from user.models import CustomUser
from .models import Event
from .views import EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView
from datetime import timedelta

class EventAPITestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = CustomUser.objects.create(username='test_user', email='test@example.com', rol='owner')
        self.user2 = CustomUser.objects.create(username='test_user2', email='test2@example.com', rol='gym')
        self.owner = Owner.objects.create(name='Owner', lastName='Owner Lastname', email='owner@example.com',
                                           phoneNumber=123456789, address='123 Owner St', userCustom=self.user)
        self.gym = Gym.objects.create(name='Test Gym', address='123 Test St', phone_number=987654321,
                                       descripcion='Test Gym Description', zip_code=54321, email='gym@example.com',
                                       owner=self.owner, userCustom=self.user2)
        self.event1 = Event.objects.create(name='Event 1',description='This is event 1',capacity=50, attendees=25, instructor='John Doe',
                                           date='2024-03-01',isClickable=True,duration=timedelta(hours=1),intensity='M',
                                           isNotice=False,gym=self.gym)

    def test_event_list_view(self):
        request = self.factory.get('/events/')
        view = EventListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_event_detail_view(self):
        request = self.factory.get('/events/')
        view = EventDetailView.as_view()
        response = view(request, pk=self.event1.pk)
        self.assertEqual(response.status_code, 200)

    def test_event_create_view(self):
        data = {'name':'Event 3','description':'This is event 3','capacity':30, 'attendees':15 , 'instructor':'Jane Smith',
                'date':'2024-03-02','isClickable':True,'duration':timedelta(hours=1),'intensity':'H',
                'isNotice':True,'gym':self.gym.pk}
        request = self.factory.post('/events/create/', data)
        view = EventCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_event_update_view(self):
        data = {'name':'Event 4','description':'This is event 4','capacity':30, 'attendees':15, 'instructor':'Jane Smith',
                'date':'2024-03-02','isClickable':True,'duration':timedelta(hours=1.5),'intensity':'H',
                'isNotice':True,'gym':self.gym.pk}
        request = self.factory.post('/events/update/', data)
        view = EventUpdateView.as_view()
        response = view(request, pk=self.event1.pk)
        self.assertEqual(response.status_code, 200)

    def test_event_delete_view(self):
        request = self.factory.delete('/events/')
        view = EventDeleteView.as_view()
        response = view(request, pk=self.event1.pk)
        self.assertEqual(response.status_code, 200)