from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Client, Gym, CustomUser
from owner.models import Owner
from .serializers import ClientSerializer
from rest_framework.permissions import BasePermission
from user.serializers import CustomUserSerializer

class IsGymOrOwner(BasePermission):
    def has_permission(self,request):
        return request.user.is_authenticated and (request.user.rol == 'gym' or request.user.rol == 'owner')

class ClientListView(APIView):
    def get(self, request):
        if request.user.rol == 'owner':
            owner=Owner.objects.get(userCustom=request.user)
            gyms=Gym.objects.filter(owner=owner)
            clients=[]
            for gym in gyms:
                clients.extend(Client.objects.filter(gym=gym))
            serializer=ClientSerializer(clients,many=True)
            return Response(serializer.data)
        elif request.user.rol == 'gym':
            gym=Gym.objects.get(userCustom=request.user)
            clients = Client.objects.filter(gym=gym)
            serializer=ClientSerializer(clients,many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)

class ClientListByGymView(APIView):
    def get(self, request,gymId):
        if (request.user.rol=='gym' and Gym.objects.get(userCustom=request.user).id==gymId) or (
                request.user.rol=='owner' and Owner.objects.get(userCustom=request.user).id==
                Gym.objects.get(pk=gymId).owner.id):
            clients = Client.objects.filter(gym=gymId)
            serializer=ClientSerializer(clients,many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)
    
class ClientDetailView(APIView):
    def get(self, request,pk):
        if request.user.rol=='client':
            clientId=Client.objects.get(user=request.user).id
            if clientId==pk:
                client = Client.objects.get(pk=pk)
                serializer=ClientSerializer(client)
                return Response(serializer.data,status=200)
            else:
                return Response(status=403)
        elif IsGymOrOwner().has_permission(request):
            client = Client.objects.get(pk=pk)
            serializer=ClientSerializer(client)
            return Response(serializer.data,status=200)
        else:
            return Response(status=403)

class ClientUsernameDetailView(APIView):
    def get(self, request,username):
        if request.user.rol=='client':
            client=Client.objects.get(user=request.user.username)
            if client.user.username==username:
                serializer=ClientSerializer(client)
                return Response(serializer.data,status=200)
            else:
                return Response(status=403)
        elif IsGymOrOwner().has_permission(request):
            client = Client.objects.get(user=request.user.username)
            serializer=ClientSerializer(client)
            return Response(serializer.data,status=200)
        else:
            return Response(status=403)
    
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
            if request.user.rol == 'gym':
                gym = Gym.objects.get(userCustom=request.user.username)
            elif request.user.rol == 'owner':
                owner=Owner.objects.get(userCustom=request.user.username)
                gym = Gym.objects.get(owner=owner)
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
    def put(self, request, pk):
        client = Client.objects.get(pk=pk)
        if IsGymOrOwner().has_permission(request) or client.user==request.user:
            client = Client.objects.get(pk=pk)
            serializer = ClientSerializer(client, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=200)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response(status=403)

class ClientDeleteView(APIView):
    def delete(self, request, pk):
        if IsGymOrOwner().has_permission(request):
            client = Client.objects.get(pk=pk)
            user = CustomUser.objects.get(username=client.user)
            client.delete()
            user.delete()
            return Response('Client deleted')
        else:
            return Response(status=403)