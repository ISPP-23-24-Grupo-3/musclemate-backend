from django.test import TestCase
from rest_framework.test import APIRequestFactory
from gym.models import Gym
from owner.models import Owner

from user.models import CustomUser
from .models import Client
from .views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView

class AssessmentTestCase(TestCase):
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

