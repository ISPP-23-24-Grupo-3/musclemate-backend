from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Client


class ClientListView(APIView):
    def get(self, request):
        clients = Client.objects.all()
        return Response(clients.data)
    
class ClientDetailView(APIView):
    def get(self, request,pk):
        client = Client.objects.get(pk=pk)
        if client:
            return Response({client.data})
        else:
            return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

class ClientCreateView(APIView):
    def post(self, request):
        client= Client(**request.data)
        client.save()
        return Response(client.data)


class ClientUpdateView(APIView):
    def post(self, request, pk):
        client = Client.objects.get(pk=pk)
        client=client.__dict__.update(request.data)
        client.save()
        return Response(client.data)

class ClientDeleteView(APIView):
    def delete(self, request, pk):
        client = Client.objects.get(pk=pk)
        client.delete()
        return Response('Client deleted')