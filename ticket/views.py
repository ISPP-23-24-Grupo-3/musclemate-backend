from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from gym.models import Gym
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from owner.models import Owner
from .models import Ticket
from .serializers import TicketSerializer, TicketViewSerializer, TicketUpdateSerializer
from rest_framework.permissions import IsAuthenticated
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
    print(gym)
    return gym

@permission_classes([IsAuthenticated])
class TicketListView(APIView):
    def get(self, request):
        tickets = Ticket.objects.all()
        serializer = TicketViewSerializer(tickets, many=True)
        return Response(serializer.data)

@permission_classes([IsAuthenticated])
class TicketListByClientView(APIView):

    def clientAuthority(self, user, client):
        has_authority = False
        if user.rol == "client":
                if getClientFromUser(user).id == client.id:
                    has_authority=True
        elif user.rol == "owner":
                if getOwnerFromUser(user).id == client.gym.owner.id:
                    has_authority=True
        elif user.rol == "gym":
                if getGymFromUser(user).id == client.gym.id:
                    has_authority=True
        return has_authority
    
    def get(self, request, clientId):
        client = Client.objects.get(id=clientId)
        user = request.user
        if self.clientAuthority(user, client):
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
                    has_authority=True
        elif user.rol == "gym":
                if getGymFromUser(user).id == equipment.gym.id:
                    has_authority=True
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
        request_user = CustomUser.objects.get(username=request.user)
        client = Client.objects.get(user=request_user)
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=client, gym=client.gym)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])    
class TicketDetailView(APIView):
    def get(self, request,pk):
        serie = Ticket.objects.get(pk=pk)
        serializer=TicketViewSerializer(serie)
        return Response(serializer.data)

@permission_classes([IsAuthenticated])
class TicketUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        ticket = self.get_object(pk)
        serializer = TicketUpdateSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        ticket = self.get_object(pk)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


