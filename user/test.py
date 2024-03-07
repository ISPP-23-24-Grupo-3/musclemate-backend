from django.test import TestCase
from django.db import transaction
from rest_framework.test import APIRequestFactory
from user.views import UserListView, UserCreateView, UserUpdateView, UserDeleteView
from user.models import CustomUser
from user.serializers import CustomUserSerializer
from rest_framework.test import force_authenticate 
class UserViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.user = CustomUser.objects.create(username='testuser', email='test@example.com', rol='client', password='testpassword', id=123456)

    def test_user_list_view(self):
        request = self.factory.get('/users/')
        view = UserListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_user_create_view(self):
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'rol': 'client', 'password': 'newpassword'}
        request = self.factory.post('/users/', data)
        view = UserCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())

    from rest_framework.test import force_authenticate  # Import the force_authenticate function

    """ def test_user_update_view(self):
        data = {'username': 'updateduser', 'email': 'updateduser@example.com', 'rol': 'client', 'password': 'updatedpassword'}
        request = self.factory.put(f'/users/update/{self.user.username}/', data)  # Change here
        force_authenticate(request, user=self.user)
        view = UserUpdateView.as_view()
        response = view(request, username=self.user.username)  # Change here
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
 """
    def test_user_delete_view(self):
        request = self.factory.delete(f'/users/{self.user.pk}/')
        view = UserDeleteView.as_view()
        response = view(request, pk=self.user.pk)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(pk=self.user.pk).exists())
