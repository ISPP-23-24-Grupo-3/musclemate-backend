from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission
from gym.models import Gym
from owner.models import Owner
from .models import Reservation
from client.models import Client
from event.models import Event
from .serializers import ReservationSerializer

class IsGymOrOwnerOrClient(BasePermission):

    def has_permission(self,request,pk):
        clientId=Reservation.objects.get(pk=pk).client.id
        gymId=Client.objects.get(pk=clientId).gym.id
        return (request.user.rol=='gym' and Gym.objects.get(userCustom=request.user).id==gymId) or (
                request.user.rol=='owner' and Owner.objects.get(userCustom=request.user).id==
                Gym.objects.get(pk=gymId).owner.id) or (request.user.rol=='client' and 
                clientId == Client.objects.get(user=request.user).id)


class ReservationListView(APIView):
    def get(self, request):
        reservations = Reservation.objects.all()
        serializer=ReservationSerializer(reservations,many=True)
        return Response(serializer.data)
    
class ReservationListByClientView(APIView):
    def get(self, request,clientId):
        gymId=Client.objects.get(pk=clientId).gym.id
        if (request.user.rol=='gym' and Gym.objects.get(userCustom=request.user).id==gymId) or (
                request.user.rol=='owner' and Owner.objects.get(userCustom=request.user).id==
                Gym.objects.get(pk=gymId).owner.id) or (request.user.rol=='client' and 
                clientId == Client.objects.get(user=request.user).id):
            client = Client.objects.get(id=clientId)
            reservations = Reservation.objects.filter(client=client)
            serializer=ReservationSerializer(reservations,many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)

class ReservationListByEventView(APIView):
    def get(self, request,eventId):
        gymId=Event.objects.get(pk=eventId).gym.id
        if (request.user.rol=='gym' and Gym.objects.get(userCustom=request.user).id==gymId) or (
                request.user.rol=='owner' and Owner.objects.get(userCustom=request.user).id==
                Gym.objects.get(pk=gymId).owner.id):
            event = Event.objects.get(id=eventId)
            reservations = Reservation.objects.filter(event=event)
            serializer=ReservationSerializer(reservations,many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)
    
class ReservationDetailView(APIView):
    def get(self, request,pk):
        if IsGymOrOwnerOrClient().has_permission(request,pk):
            reservation = Reservation.objects.get(pk=pk)
            serializer=ReservationSerializer(reservation)
            return Response(serializer.data)
        else:
            return Response(status=403)

class ReservationCreateView(APIView):
    def post(self, request):
        clientId=Client.objects.get(pk=request.data.get('client')).id
        gymId=Client.objects.get(pk=clientId).gym.id
        if (request.user.rol=='gym' and Gym.objects.get(userCustom=request.user).id==gymId) or (
                request.user.rol=='owner' and Owner.objects.get(userCustom=request.user).id==
                Gym.objects.get(pk=gymId).owner.id) or request.user.rol=='client':
            event=Event.objects.get(pk=request.data.get('event'))
            if(event.capacity>event.attendees and not Reservation.objects.filter(
                    client=clientId, event=event.id).exists()):
                serializer = ReservationSerializer(data=request.data)
                if serializer.is_valid():
                    event.attendees=event.attendees+1
                    Event.save(event)
                    serializer.save()
                    return Response(serializer.data, status=201)
                else:
                    return Response(serializer.errors, status=400)
            else:
                if event.capacity<=event.attendees:
                    return Response('El evento esta lleno',status=400)
                else:
                    return Response('El cliente ya esta registrado en este evento',status=400)
        else:
            return Response(status=403)

class ReservationUpdateView(APIView):
    def post(self, request, pk):
        if IsGymOrOwnerOrClient().has_permission(request,pk):
            reservation = Reservation.objects.get(pk=pk)
            serializer = ReservationSerializer(reservation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        else:
            return Response(status=403)

class ReservationDeleteView(APIView):
    def delete(self, request, pk):
        if IsGymOrOwnerOrClient().has_permission(request,pk):
            reservation = Reservation.objects.get(pk=pk)
            event=reservation.event
            event.attendees=event.attendees-1
            Event.save(event)
            reservation.delete()
            return Response('Reservation deleted')
        else:
            return Response(status=403)
