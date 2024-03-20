from rest_framework.response import Response
from rest_framework.views import APIView
from client.models import Client
from owner.models import Owner
from .models import Event,Gym
from reservation.models import Reservation
from .serializers import EventSerializer


class EventListView(APIView):
    def get(self, request):
        if request.user.rol=='gym' or request.user.rol=='owner':
            events = Event.objects.all()
            serializer=EventSerializer(events,many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)
        
class EventListByGymView(APIView):
    def get(self, request,gymId):
        if (request.user.rol=='gym' and Gym.objects.get(userCustom=request.user).id==gymId) or (
                request.user.rol=='owner' and Owner.objects.get(userCustom=request.user).id==
                Gym.objects.get(pk=gymId).owner.id) or (request.user.rol=='client'
                and Client.objects.get(user=request.user).gym.id==gymId):
            events = Event.objects.filter(gym=gymId)
            serializer=EventSerializer(events,many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)

class EventListByClientView(APIView):
    def get(self, request, clientId):
        client = Client.objects.get(id = clientId)
        gymId = Gym.objects.get(id = client.gym.id).id
        if (request.user.rol=='gym' and Gym.objects.get(userCustom=request.user).id==gymId) or (
                request.user.rol=='owner' and Owner.objects.get(userCustom=request.user).id==
                Gym.objects.get(pk=gymId).owner.id) or (request.user.rol=='client'
                and Client.objects.get(user=request.user).gym.id==gymId):
            reservations = Reservation.objects.filter(client = client.id)
            events = []
            for reservation in reservations:
                events.append(reservation.event)
            serializer = EventSerializer(events,many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)


class EventDetailView(APIView):
    def get(self, request,pk):
        gymId=Event.objects.get(pk=pk).gym.id
        if (request.user.rol=='gym' and Gym.objects.get(userCustom=request.user).id==gymId) or (
                request.user.rol=='owner' and Owner.objects.get(userCustom=request.user).id==
                Owner.objects.get(gym=gymId).id) or (request.user.rol=='client'
                and Client.objects.get(user=request.user).gym.id==gymId):
            event = Event.objects.get(pk=pk)
            serializer=EventSerializer(event)
            return Response(serializer.data)
        else:
            return Response(status=403)


class EventCreateView(APIView):
    def post(self, request):
        gymId=int(request.data.get('gym'))
        if (request.user.rol=='gym' and Gym.objects.get(userCustom=request.user).id==gymId) or (
                request.user.rol=='owner' and Owner.objects.get(userCustom=request.user).id==
                Owner.objects.get(gym=gymId).id):
            serializer = EventSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response(status=403)


class EventUpdateView(APIView):
    def post(self, request, pk):
        gym=Event.objects.get(pk=pk).gym
        if (request.user.rol=='gym' and Gym.objects.get(userCustom=request.user).id==gym.id) or (
                request.user.rol=='owner' and Owner.objects.get(userCustom=request.user).id==
                gym.owner.id):
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        else:
            return Response(status=403)

class EventDeleteView(APIView):
    def delete(self, request, pk):
        gym=Event.objects.get(pk=pk).gym
        if (request.user.rol=='gym' and Gym.objects.get(userCustom=request.user).id==gym.id) or (
                request.user.rol=='owner' and Owner.objects.get(userCustom=request.user).id==
                gym.owner.id):
            event = Event.objects.get(pk=pk)
            event.delete()
            return Response('Event deleted')
        else:
            return Response(status=403)