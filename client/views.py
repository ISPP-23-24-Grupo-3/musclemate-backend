from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Client
from .serializers import ClientSerializer
from .serializers import UserSerializer


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
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save(role='client')
            client_serializer = ClientSerializer(data=request.data)
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