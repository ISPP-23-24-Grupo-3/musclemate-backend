from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from gym.models import Gym
from owner.models import Owner
from user.models import CustomUser
from .models import Client,Ticket,Equipment
from .views import TicketCreateView,TicketListView,TicketDeleteView,TicketDetailView,TicketUpdateView,TicketListByClientView,TicketListByEquipmentView

class TicketTests(TestCase):
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
        self.equipment=Equipment.objects.create(name= 'Mancuernas',brand= 'Marca A',serial_number='MNCD002',
                description= 'Un par de mancuernas de 5 kg cada una',muscular_group= 'arms',gym= self.gym)
        self.ticket=Ticket.objects.create(label= 'Ticket 1',description= 'Description of ticket 1',status= True,
            date='2023-12-30',gym= self.gym,client= self.client,equipment= self.equipment)

    #test del list view
    def test_tickets_list_view_how_gym(self):
        request = self.factory.get('/tickets/')
        force_authenticate(request, user=self.userGym)
        view = TicketListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_tickets_list_view_how_owner(self):
        request = self.factory.get('/tickets/')
        force_authenticate(request, user=self.userOwner)
        view = TicketListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)


    #test del list by client id view
    def test_tickets_list_by_clientId_view_how_gym(self):
        request = self.factory.get('/tickets/byClient/')
        force_authenticate(request, user=self.userGym)
        view = TicketListByClientView.as_view()
        response = view(request,clientId=self.client.id)
        self.assertEqual(response.status_code, 200)

    def test_tickets_list_by_clientId_view_how_owner(self):
        request = self.factory.get('/tickets/byClient/')
        force_authenticate(request, user=self.userOwner)
        view = TicketListByClientView.as_view()
        response = view(request,clientId=self.client.id)
        self.assertEqual(response.status_code, 200)

    def test_tickets_list_by_clientId_view_how_client(self):
        request = self.factory.get('/tickets/byClient/')
        force_authenticate(request, user=self.userClient)
        view = TicketListByClientView.as_view()
        response = view(request,clientId=self.client.id)
        self.assertEqual(response.status_code, 200)


    #test del list by equipment id view
    def test_tickets_list_by_equipmentId_view_how_gym(self):
        request = self.factory.get('/tickets/byEquipment')
        force_authenticate(request, user=self.userGym)
        view = TicketListByEquipmentView.as_view()
        response = view(request,equipmentId=self.equipment.id)
        self.assertEqual(response.status_code, 200)

    def test_tickets_list_by_equipmentId_view_how_owner(self):
        request = self.factory.get('/tickets/byEquipment')
        force_authenticate(request, user=self.userOwner)
        view = TicketListByEquipmentView.as_view()
        response = view(request,equipmentId=self.equipment.id)
        self.assertEqual(response.status_code, 200)


    #test del detail view
    def test_tickets_detail_view_how_client(self):
        request = self.factory.get('/tickets/detail/')
        force_authenticate(request, user=self.userClient)
        view = TicketDetailView.as_view()
        response = view(request, pk=self.ticket.pk)
        self.assertEqual(response.status_code, 200)

    def test_tickets_detail_view_how_gym(self):
        request = self.factory.get('/tickets/detail/')
        force_authenticate(request, user=self.userGym)
        view = TicketDetailView.as_view()
        response = view(request, pk=self.ticket.pk)
        self.assertEqual(response.status_code, 200)

    def test_tickets_detail_view_how_owner(self):
        request = self.factory.get('/tickets/detail/')
        force_authenticate(request, user=self.userOwner)
        view = TicketDetailView.as_view()
        response = view(request, pk=self.ticket.pk)
        self.assertEqual(response.status_code, 200)


    #test create view
    def test_tickets_create_view_how_client(self):
        data = {'label': 'Ticket 1','description': 'Description of ticket 1','status': True,'date': '2023-12-30',
            'gym': self.gym.pk,'client': self.client.pk,'equipment': self.equipment.pk}
        request = self.factory.post('/tickets/create/',data)
        force_authenticate(request, user=self.userClient)
        view = TicketCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)


    #test update view
    def test_ticket_update_view_how_client(self):
        data = {'label': 'Updated Ticket 1','description': 'Description of ticket 1','status': True,'date': '2023-12-30',
            'gym': self.gym.pk,'client': self.client.pk,'equipment': self.equipment.pk}
        request = self.factory.put('/tickets/update/',data)
        force_authenticate(request, user=self.userClient)
        view = TicketUpdateView.as_view()
        response = view(request, pk=self.ticket.pk)
        self.assertEqual(response.status_code, 200)

    def test_ticket_update_view_how_owner(self):
        data = {'label': 'Updated Ticket 1','description': 'Description of ticket 1','status': True,'date': '2023-12-30',
            'gym': self.gym.pk,'client': self.client.pk,'equipment': self.equipment.pk}
        request = self.factory.put('/tickets/update/',data)
        force_authenticate(request, user=self.userOwner)
        view = TicketUpdateView.as_view()
        response = view(request, pk=self.ticket.pk)
        self.assertEqual(response.status_code, 200)

    def test_ticket_update_view_how_gym(self):
        data = {'label': 'Updated Ticket 1','description': 'Description of ticket 1','status': True,'date': '2023-12-30',
            'gym': self.gym.pk,'client': self.client.pk,'equipment': self.equipment.pk}
        request = self.factory.put('/tickets/update/',data)
        force_authenticate(request, user=self.userGym)
        view = TicketUpdateView.as_view()
        response = view(request, pk=self.ticket.pk)
        self.assertEqual(response.status_code, 200)


    #test delete view
    def test_ticket_delete_view_how_gym(self):
        request = self.factory.delete('/tickets/')
        force_authenticate(request, user=self.userGym)
        view = TicketDeleteView.as_view()
        response = view(request, pk=self.ticket.pk)
        self.assertEqual(response.status_code, 204)

    def test_ticket_delete_view_how_client(self):
        request = self.factory.delete('/tickets/')
        force_authenticate(request, user=self.userClient)
        view = TicketDeleteView.as_view()
        response = view(request, pk=self.ticket.pk)
        self.assertEqual(response.status_code, 204)

    def test_ticket_delete_view_how_owner(self):
        request = self.factory.delete('/tickets/')
        force_authenticate(request, user=self.userOwner)
        view = TicketDeleteView.as_view()
        response = view(request, pk=self.ticket.pk)
        self.assertEqual(response.status_code, 204)