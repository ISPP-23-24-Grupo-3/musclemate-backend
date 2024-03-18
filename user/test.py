from django.test import TestCase
from rest_framework.test import APIRequestFactory
from user.views import UserListView, UserCreateView, UserDeleteView, UserUpdateView
from user.models import CustomUser
from rest_framework.test import force_authenticate 
class UserViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.user = CustomUser.objects.create(username='testuser', email='testprueba@example.com', rol='client', password='testpassword', id=123456)
        cls.userAdmin = CustomUser.objects.create(username='testuser1', email='test2@example.com', rol='admin',
            is_staff=True,password='testpassword', id=123457)
    def test_user_list_view(self):
        request = self.factory.get('/users/')
        force_authenticate(request, user=self.userAdmin)
        view = UserListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_user_create_view(self):
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'rol': 'client', 'password': 'newpassword'}
        request = self.factory.post('/users/', data)
        force_authenticate(request, user=self.userAdmin)
        view = UserCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())

    def test_user_update_view(self):
        data = {'username': 'testuser', 'email': 'updateduser@example.com', 'rol': 'client', 'password': 'updatedpassword'}
        request = self.factory.put(f'/users/update/{self.user.username}/', data)
        force_authenticate(request, user=self.userAdmin)
        view = UserUpdateView.as_view()
        response = view(request, username=self.user.username)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser')

    def test_user_delete_view(self):
        request = self.factory.delete(f'/users/{self.user.pk}/')
        force_authenticate(request, user=self.userAdmin)
        view = UserDeleteView.as_view()
        response = view(request, pk=self.user.pk)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(pk=self.user.pk).exists())
