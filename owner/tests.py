from django.test import TestCase
from rest_framework.test import APIRequestFactory
from user.models import CustomUser
from .models import Owner
from .views import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

class OwnerAPITestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create(username='testuser', email='test@example.com',
            rol='owner', password='testpassword')
        self.user1 = CustomUser.objects.create(username='test_user_1', email='test1@example.com',
            rol='owner',password='testpassword')
        self.owner = Owner.objects.create(
            name='John',
            lastName='Doe',
            email='john.doe@example.com',
            phoneNumber=123456789,
            address='123 Owner St',
            userCustom=self.user
        )

    def test_owner_list_view(self):
        request = self.factory.get('d')
        view = OwnerListView.as_view()
        response=view(request)
        self.assertEqual(response.status_code, 200)

    def test_owner_detail_view(self):
        request = self.factory.get('/owners/detail/')
        response = OwnerDetailView.as_view()(request, pk=self.owner.userCustom)
        self.assertEqual(response.status_code, 200)

    def test_owner_create_view(self):
        data = {"name": "John","lastName": "Doe","email": "foo@bar.com","phoneNumber": 614869725,
            "address": "Fake st","userCustom": {"username": "testOwner","password": "musclemate123"}}
        request = self.factory.post('/owners/create/', data, format='json')
        response = OwnerCreateView.as_view()(request)
        self.assertEqual(response.status_code, 201)

    def test_owner_update_view(self):
        data = {'name':'Update','lastName':'Doe','email':'john.doe2@example.com','phoneNumber':123456789,
                'address':'123 Owner St','userCustom':self.user.pk}
        request = self.factory.put('/owners/update/', data)
        response = OwnerUpdateView.as_view()(request, pk=self.owner.pk)
        self.assertEqual(response.status_code, 200)

    def test_owner_delete_view(self):
        request = self.factory.delete('/owners/delete/')
        response = OwnerDeleteView.as_view()(request, pk=self.owner.pk)
        self.assertEqual(response.status_code, 200)