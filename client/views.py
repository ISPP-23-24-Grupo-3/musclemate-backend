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
        if IsGymOrOwner().has_permission(request):
            clients = Client.objects.all()
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
        if IsGymOrOwner().has_permission(request):
            user_serializer = CustomUserSerializer(data=request.data)
            if user_serializer.is_valid():
                user = user_serializer.save(rol='client')
                clientData = request.data.dict()
                clientData["user"] = user.username
                client_serializer = ClientSerializer(data=clientData)
                if client_serializer.is_valid():
                    client_serializer.save()
                    return Response(client_serializer.data, status=201)
                else:
                    CustomUser.objects.get(username = user.username).delete()
                    return Response(client_serializer.errors, status=400)
            else:
                return Response(user_serializer.errors, status=400)
        else:
            return Response(status=403)

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