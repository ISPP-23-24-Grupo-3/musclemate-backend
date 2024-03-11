from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Client, Gym
from .serializers import ClientSerializer
from user.serializers import CustomUserSerializer

class ClientListView(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer=ClientSerializer(clients,many=True)
        return Response(serializer.data)
    
class ClientDetailView(APIView):
    def get(self, request,pk):
        client = Client.objects.get(pk=pk)
        serializer=ClientSerializer(client)
        return Response(serializer.data)
        
class ClientCreateView(APIView):
    def post(self, request):
        if request.user.rol == 'client':
            return Response('You are not authorized to create a client')
    
        user_data = request.data.get('userCustom')
        user_serializer = CustomUserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save(rol='client')
            client_data = request.data
            client_data['user'] = user.username  # Pass the primary key of the user
            client_serializer = ClientSerializer(data=client_data)
            gym = Gym.objects.get(userCustom=request.user.username)
            client_data['gym'] = gym.id
            client_data['register'] = True
            client_serializer = ClientSerializer(data=client_data)
            if client_serializer.is_valid():
                client_serializer.save(user=user)
                return Response(client_serializer.data, status=201)
            else:
                return Response(client_serializer.errors, status=400)
        else:
            return Response(user_serializer.errors, status=400)


class ClientUpdateView(APIView):
    def post(self, request, pk):
        client = Client.objects.get(pk=pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class ClientDeleteView(APIView):
    def delete(self, request, pk):
        client = Client.objects.get(pk=pk)
        client.delete()
        return Response('Client deleted')