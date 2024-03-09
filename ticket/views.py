from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ticket
from .serializers import TicketSerializer, TicketViewSerializer
from rest_framework.permissions import IsAuthenticated
from client.models import Client
from user.models import CustomUser

class TicketListView(APIView):
    def get(self, request):
        tickets = Ticket.objects.all()
        serializer = TicketViewSerializer(tickets, many=True)
        return Response(serializer.data)

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
    
class TicketDetailView(APIView):
    def get(self, request,pk):
        serie = Ticket.objects.get(pk=pk)
        serializer=TicketViewSerializer(serie)
        return Response(serializer.data)

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


