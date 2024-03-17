from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from owner.models import Owner
from client.models import Client
from user.models import CustomUser
from .models import Equipment,Gym
from .views import EquipmentCreateView,EquipmentDeleteView,EquipmentDetailView,EquipmentListView,EquipmentUpdateView,EquipmentObtainTime

class ClientTests(TestCase):
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
        self.client = Client.objects.create(name='Client 1', lastName='Lastname 1', email='client1@example.com',
            birth='2000-01-01', zipCode=12345, gender='M', phoneNumber=123456789,address='123 Test St',
            city='Test City', register=True,user=self.userClient,gym=self.gym)
        self.equipment=Equipment.objects.create(name= 'Mancuernas',brand= 'Marca A',serial_number='MNCD001',
                description= 'Un par de mancuernas de 5 kg cada una',muscular_group= 'arms',gym= self.gym)

    #test del list view
    def test_equipment_list_view_how_gym(self):
        request = self.factory.get('/equipments/')
        force_authenticate(request, user=self.userGym)
        view = EquipmentListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_equipment_list_view_how_owner(self):
        request = self.factory.get('/equipments/')
        force_authenticate(request, user=self.userOwner)
        view = EquipmentListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
    
    def test_equipment_list_view_how_owner(self):
        request = self.factory.get('/equipments/')
        force_authenticate(request, user=self.userClient)
        view = EquipmentListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)


    #test del detail view
    def test_equipment_detail_view_how_gym(self):
        request = self.factory.get('/equipments/detail/')
        force_authenticate(request, user=self.userGym)
        view = EquipmentDetailView.as_view()
        response = view(request, pk=self.equipment.pk)
        self.assertEqual(response.status_code, 200)

    def test_equipment_detail_view_how_owner(self):
        request = self.factory.get('/equipments/detail/')
        force_authenticate(request, user=self.userOwner)
        view = EquipmentDetailView.as_view()
        response = view(request, pk=self.equipment.pk)
        self.assertEqual(response.status_code, 200)

    def test_equipment_detail_view_how_client(self):
        request = self.factory.get('/equipments/detail/')
        force_authenticate(request, user=self.userClient)
        view = EquipmentDetailView.as_view()
        response = view(request, pk=self.equipment.pk)
        self.assertEqual(response.status_code, 200)


    #test create view
    def test_equipment_create_view_how_owner(self):
        data = {'name': 'New Equipment','brand': 'Marca A','serial_number':'MNCD002',
            'description': 'Un par de mancuernas de 5 kg cada una','muscular_group': 'arms','gym': self.gym.id}
        request = self.factory.post('/equipments/create/',data)
        force_authenticate(request, user=self.userOwner)
        view = EquipmentCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)


    #test update view
    def test_equipment_update_view_how_owner(self):
        data = {'name': 'Update Equipment','brand': 'Marca A','serial_number':'MNCD001',
            'description': 'Un par de mancuernas de 5 kg cada una','muscular_group': 'arms','gym': self.gym.pk}
        request = self.factory.put('/equipments/update/',data)
        force_authenticate(request, user=self.userOwner)
        view = EquipmentUpdateView.as_view()
        response = view(request, pk=self.equipment.pk)
        self.assertEqual(response.status_code, 200)


    #test delete view
    def test_equipment_delete_view_how_owner(self):
        request = self.factory.delete('/equipments/')
        force_authenticate(request, user=self.userOwner)
        view = EquipmentDeleteView.as_view()
        response = view(request, pk=self.equipment.pk)
        self.assertEqual(response.status_code, 204)


    #test del obtain time view
    def test_equipment_obtain_time_view_how_owner(self):
        request = self.factory.get('/equipments/time/')
        force_authenticate(request, user=self.userOwner)
        view = EquipmentObtainTime.as_view()
        response = view(request, pk=self.equipment.pk)
        self.assertEqual(response.status_code, 200)