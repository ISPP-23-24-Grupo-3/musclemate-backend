from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from gym.models import Gym
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from owner.models import Owner
from .models import Ticket
from .serializers import TicketSerializer, TicketViewSerializer, TicketUpdateSerializer
from client.models import Client
from user.models import CustomUser
from equipment.models import Equipment


def getClientFromUser(username):
    user = CustomUser.objects.get(username=username)
    client = Client.objects.get(user=user)
    return client


def getOwnerFromUser(username):
    user = CustomUser.objects.get(username=username)
    owner = Owner.objects.get(userCustom=user)
    return owner


def getGymFromUser(username):
    user = CustomUser.objects.get(username=username)
    gym = Gym.objects.get(userCustom=user)
    return gym


def clientAuthority(user, client):
    has_authority = False
    username = user.username
    if user.rol == "client":
        if getClientFromUser(username).id == client.id:
            has_authority = True
    elif user.rol == "owner":
        if getOwnerFromUser(username).id == client.gym.owner.id:
            has_authority = True
    elif user.rol == "gym":
        if getGymFromUser(username).id == client.gym.id:
            has_authority = True
    return has_authority


@permission_classes([IsAuthenticated])
class TicketListView(APIView):
    def get(self, request):
        if request.user.rol != "client":
            if request.user.rol == "owner":
                tickets = []
                gyms = Gym.objects.filter(
                    owner=getOwnerFromUser(request.user)
                )  # puede devolver varios gimnasios
                for gym in gyms:
                    tickets.extend(Ticket.objects.filter(gym=gym))
                serializer = TicketViewSerializer(tickets, many=True)
                return Response(serializer.data)
            else:
                gym = getGymFromUser(request.user)
                tickets = Ticket.objects.filter(gym=gym)
                serializer = TicketViewSerializer(tickets, many=True)
                return Response(serializer.data)
        else:
            return Response(status=403)


@permission_classes([IsAuthenticated])
class TicketListByClientView(APIView):
    def get(self, request, clientId):
        client = Client.objects.get(id=clientId)
        user = request.user
        if clientAuthority(user, client):
            tickets = Ticket.objects.filter(client=client)
            serializer = TicketViewSerializer(tickets, many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)


@permission_classes([IsAuthenticated])
class TicketListByEquipmentView(APIView):
    def equipmentAuthority(self, user, equipment):
        has_authority = False
        if user.rol == "owner":
            if getOwnerFromUser(user).id == equipment.gym.owner.id:
                has_authority = True
        elif user.rol == "gym":
            if getGymFromUser(user).id == equipment.gym.id:
                has_authority = True
        elif user.rol == "client":
            client = Client.objects.get(user=user)
            if equipment.gym.id == client.gym.id:
                has_authority = True
        return has_authority

    def get(self, request, equipmentId):
        equipment = Equipment.objects.get(id=equipmentId)
        user = request.user
        if self.equipmentAuthority(user, equipment):
            tickets = Ticket.objects.filter(equipment=equipment, gym=equipment.gym)
            serializer = TicketViewSerializer(tickets, many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)


@permission_classes([IsAuthenticated])
class TicketCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.rol == "client":
            request_user = CustomUser.objects.get(username=request.user)
            client = Client.objects.get(user=request_user)
            serializer = TicketSerializer(data=request.data)
            if serializer.is_valid():
                ticket = serializer.save(client=client, gym=client.gym)
                if "image" in request.FILES:
                    ticket.image = request.FILES["image"]
                    ticket.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=403)


@permission_classes([IsAuthenticated])
class TicketDetailView(APIView):
    def get(self, request, pk):
        ticket = Ticket.objects.get(pk=pk)
        if clientAuthority(request.user, ticket.client):
            serializer = TicketViewSerializer(ticket)
            return Response(serializer.data)
        else:
            return Response(status=403)


@permission_classes([IsAuthenticated])
class TicketUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        ticket = self.get_object(pk)
        if clientAuthority(request.user, ticket.client):
            serializer = TicketUpdateSerializer(ticket, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if "image" in request.FILES:
                    ticket = self.get_object(pk)
                    ticket.image = request.FILES["image"]
                    ticket.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=403)


@permission_classes([IsAuthenticated])
class TicketDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        ticket = self.get_object(pk)
        if clientAuthority(request.user, ticket.client):
            ticket.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=403)
