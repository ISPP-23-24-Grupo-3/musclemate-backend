from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Reservation
from client.models import Client



class ReservationListView(APIView):
    def get(self, request):
        reservations = Reservation.objects.all()
        return Response(reservations.data)
    
class ReservationListByClientView(APIView):
    def get(self, request):
        client = Client.objects.get(user=request.user)
        reservations = Reservation.objects.filter(client=client)
        return Response(reservations.data)
    
class ReservationDetailView(APIView):
    def get(self, request,pk):
        reservation = Reservation.objects.get(pk=pk)
        if reservation:
            return Response({reservation.data})
        else:
            return Response({"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)

class ReservationCreateView(APIView):
    def post(self, request):
        reservation= Reservation(**request.data)
        reservation.save()
        return Response(reservation.data)


class ReservationUpdateView(APIView):
    def post(self, request, pk):
        reservation = Reservation.objects.get(pk=pk)
        reservation=reservation.__dict__.update(request.data)
        reservation.save()
        return Response(reservation.data)

class ReservationDeleteView(APIView):
    def delete(self, request, pk):
        reservation = Reservation.objects.get(pk=pk)
        reservation.delete()
        return Response('Reservation deleted')
