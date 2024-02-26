from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Reservation
from client.models import Client
from .serializers import ReservationSerializer



class ReservationListView(APIView):
    def get(self, request):
        reservations = Reservation.objects.all()
        serializer=ReservationSerializer(reservations,many=True)
        return Response(serializer.data)
    
class ReservationListByClientView(APIView):
    def get(self, request):
        client = Client.objects.get(user=request.user)
        reservations = Reservation.objects.filter(client=client)
        serializer=ReservationSerializer(reservations,many=True)
        return Response(serializer.data)
    
class ReservationDetailView(APIView):
    def get(self, request,pk):
        reservation = Reservation.objects.get(pk=pk)
        serializer=ReservationSerializer(reservation)
        return Response(serializer.data)

class ReservationCreateView(APIView):
    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class ReservationUpdateView(APIView):
    def post(self, request, pk):
        reservation = Reservation.objects.get(pk=pk)
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class ReservationDeleteView(APIView):
    def delete(self, request, pk):
        reservation = Reservation.objects.get(pk=pk)
        reservation.delete()
        return Response('Reservation deleted')
