from django.test import TestCase
from rest_framework.test import APIRequestFactory
from user.models import CustomUser
from .models import Owner
from .views import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from rest_framework.test import force_authenticate

class OwnerAPITestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create(username='testuser', email='test@example.com',
            rol='owner', password='testpassword')
        self.user1 = CustomUser.objects.create(username='test_user_1', email='test1@example.com',
            rol='owner',password='testpassword')
        self.owner = Owner.objects.create(
            name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone_number=123456789,
            address='123 Owner St',
            userCustom=self.user
        )
        self.userAdmin = CustomUser.objects.create(username='admin', email='admin@gmail.com',
            rol='admin', password='admin123')

    def test_owner_list_view(self):
        request = self.factory.get('/owners/')
        self.userAdmin.is_superuser = True
        force_authenticate(request, user=self.userAdmin)
        view = OwnerListView.as_view()
        response=view(request)
        self.assertEqual(response.status_code, 200)

    def test_owner_detail_view(self):
        request = self.factory.get('/owners/detail/')
        self.userAdmin.is_superuser = True
        force_authenticate(request, user=self.userAdmin)
        response = OwnerDetailView.as_view()(request, pk=self.owner.userCustom)
        self.assertEqual(response.status_code, 200)

    def test_owner_create_view(self):
        data = {"name": "John","last_name": "Doe","email": "foo@bar.com","phone_number": 614869725,
            "address": "Fake st","userCustom":{ "username": "testOwner","password": "musclemate123"}}
        request = self.factory.post('/owners/create/', data, format='json')
        self.userAdmin.is_superuser = True
        force_authenticate(request, user=self.userAdmin)
        response = OwnerCreateView.as_view()(request)
        self.assertEqual(response.status_code, 201)

    def test_owner_create_view_error_phone_number(self):
        data = {"name": "John","last_name": "Doe","email": "foo@bar.com","phone_number": 1,
            "address": "Fake st","userCustom":{ "username": "testOwner","password": "musclemate123"}}
        request = self.factory.post('/owners/create/', data, format='json')
        self.userAdmin.is_superuser = True
        force_authenticate(request, user=self.userAdmin)
        response = OwnerCreateView.as_view()(request)
        self.assertIn('El número de teléfono debe contener solo dígitos y una longitud de 9 dígitos.',response.data['phone_number'][0])

    def test_owner_update_view(self):
        data = {'name':'Update','last_name':'Doe','email':'john.doe2@example.com','phone_number':123456789,
                'address':'123 Owner St','userCustom':self.user.pk}
        request = self.factory.put('/owners/update/', data)
        self.userAdmin.is_superuser = True
        force_authenticate(request, user=self.userAdmin)
        response = OwnerUpdateView.as_view()(request, pk=self.owner.userCustom)
        self.assertEqual(response.status_code, 200)

    def test_owner_delete_view(self):
        request = self.factory.delete('/owners/delete/')
        self.userAdmin.is_superuser = True
        force_authenticate(request, user=self.userAdmin)
        response = OwnerDeleteView.as_view()(request, pk=self.owner.pk)
        self.assertEqual(response.status_code, 200)