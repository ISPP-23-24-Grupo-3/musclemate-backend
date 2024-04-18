from django.test import TestCase
from rest_framework.test import APIRequestFactory,force_authenticate
from gym.models import Gym
from owner.models import Owner
from user.models import CustomUser
from .models import Client,Assessment,Equipment
from .views import (
    AssessmentListView,
    AssessmentCreateView,
    AssessmentDeleteView,
    AssessmentDetailView,
    AssessmentUpdateView,
    AssessmentListByClientView,
    AssessmentListByEquipmentView
)

class AssessmentTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.userClient = CustomUser.objects.create(username='test_user', email='test@example.com', rol='client')
        self.userGym = CustomUser.objects.create(username='test_user_2', email='test2@example.com', rol='gym')
        self.userOwner = CustomUser.objects.create(username='test_user_3', email='test3@example.com', rol='owner')
        self.userClient2 = CustomUser.objects.create(username='test_user_4', email='test4@example.com', rol='client')

        self.owner = Owner.objects.create(name='Owner', last_name='Owner last_name', email='owner@example.com',
            phone_number=123456789, address='123 Owner St', userCustom=self.userOwner)
        self.gym = Gym.objects.create(name='Test Gym', address='123 Test St', phone_number=987654321,
            descripcion='Test Gym Description', zip_code=54321, email='gym@example.com',
            owner=self.owner, userCustom=self.userGym)
        self.client = Client.objects.create(name='Client 1', last_name='last_name 1', email='client1@example.com',
            birth='2000-01-01', zipCode=12345, gender='M', phone_number=123456789,address='123 Test St',
            city='Test City', register=True,user=self.userClient,gym=self.gym)
        self.client2 = Client.objects.create(name='Client 2', last_name='last_name 2', email='client2@example.com',
            birth='2000-01-01', zipCode=12345, gender='M', phone_number=123456788,address='123 Test St',
            city='Test City', register=True,user=self.userClient2,gym=self.gym)
        self.equipment=Equipment.objects.create(name= 'Mancuernas',brand= 'Marca A',serial_number='MNCD001',
                description= 'Un par de mancuernas de 5 kg cada una',muscular_group= 'arms',gym= self.gym)
        self.assessment=Assessment.objects.create(stars= 5,equipment= self.equipment,client= self.client)


    #test del list view
    def test_assessment_list_view_how_gym(self):
        request = self.factory.get('/assessments/')
        force_authenticate(request, user=self.userGym)
        view = AssessmentListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_assessment_list_view_how_owner(self):
        request = self.factory.get('/assessments/')
        force_authenticate(request, user=self.userOwner)
        view = AssessmentListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)


    #test del list by client id view
    def test_assessment_list_by_clientId_view_how_gym(self):
        request = self.factory.get('/assessments/client/')
        force_authenticate(request, user=self.userGym)
        view = AssessmentListByClientView.as_view()
        response = view(request,clientId=self.client.id)
        self.assertEqual(response.status_code, 200)

    def test_assessment_list_by_clientId_view_how_owner(self):
        request = self.factory.get('/assessments/client/')
        force_authenticate(request, user=self.userOwner)
        view = AssessmentListByClientView.as_view()
        response = view(request,clientId=self.client.id)
        self.assertEqual(response.status_code, 200)

    def test_assessment_list_by_clientId_view_how_client(self):
        request = self.factory.get('/assessments/client/')
        force_authenticate(request, user=self.userClient)
        view = AssessmentListByClientView.as_view()
        response = view(request,clientId=self.client.id)
        self.assertEqual(response.status_code, 200)


    #test del list by equipment id view
    def test_assessment_list_by_equipmentId_view_how_gym(self):
        request = self.factory.get('/assessments/equipment/')
        force_authenticate(request, user=self.userGym)
        view = AssessmentListByEquipmentView.as_view()
        response = view(request,equipmentId=self.equipment.id)
        self.assertEqual(response.status_code, 200)

    def test_assessment_list_by_equipmentId_view_how_owner(self):
        request = self.factory.get('/assessments/equipment/')
        force_authenticate(request, user=self.userOwner)
        view = AssessmentListByEquipmentView.as_view()
        response = view(request,equipmentId=self.equipment.id)
        self.assertEqual(response.status_code, 200)

    def test_assessment_list_by_equipmentId_view_how_client(self):
        request = self.factory.get('/assessments/equipment/')
        force_authenticate(request, user=self.userClient)
        view = AssessmentListByEquipmentView.as_view()
        response = view(request,equipmentId=self.equipment.id)
        self.assertEqual(response.status_code, 200)


    #test del detail view
    def test_assessment_detail_view_how_client(self):
        request = self.factory.get('/assessments/detail/')
        force_authenticate(request, user=self.userClient)
        view = AssessmentDetailView.as_view()
        response = view(request, pk=self.assessment.pk)
        self.assertEqual(response.status_code, 200)

    def test_assessment_detail_view_how_gym(self):
        request = self.factory.get('/assessments/detail/')
        force_authenticate(request, user=self.userGym)
        view = AssessmentDetailView.as_view()
        response = view(request, pk=self.assessment.pk)
        self.assertEqual(response.status_code, 200)

    def test_assessment_detail_view_how_owner(self):
        request = self.factory.get('/assessments/detail/')
        force_authenticate(request, user=self.userOwner)
        view = AssessmentDetailView.as_view()
        response = view(request, pk=self.assessment.pk)
        self.assertEqual(response.status_code, 200)

    #test create view
    def test_assessment_create_view_how_client(self):
        data = {'stars': 5,'equipment': self.equipment.pk,'client': self.client2.pk}
        request = self.factory.post('/assessments/create/',data)
        force_authenticate(request, user=self.userClient)
        view = AssessmentCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)


    #test update view
    def test_assessment_update_view_how_client(self):
        data = {'stars': 3,'equipment': self.equipment.pk,'client': self.client.pk}
        request = self.factory.put('/assessments/update/',data)
        force_authenticate(request, user=self.userClient)
        view = AssessmentUpdateView.as_view()
        response = view(request, pk=self.assessment.pk)
        self.assertEqual(response.status_code, 200)


    #test delete view
    def test_assessment_delete_view_how_client(self):
        request = self.factory.delete('/assessments/')
        force_authenticate(request, user=self.userClient)
        view = AssessmentDeleteView.as_view()
        response = view(request, pk=self.assessment.pk)
        self.assertEqual(response.status_code, 204)

