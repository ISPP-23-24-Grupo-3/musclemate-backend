from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Client
from .serializers import ClientSerializer


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
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


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