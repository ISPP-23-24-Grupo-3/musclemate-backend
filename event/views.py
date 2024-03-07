from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Event
from .serializers import EventSerializer



class EventListView(APIView):
    def get(self, request):
        events = Event.objects.all()
        serializer=EventSerializer(events,many=True)
        return Response(serializer.data)
    
class EventDetailView(APIView):
    def get(self, request,pk):
        event = Event.objects.get(pk=pk)
        serializer=EventSerializer(event)
        return Response(serializer.data)

class EventCreateView(APIView):
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class EventUpdateView(APIView):
    def post(self, request, pk):
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class EventDeleteView(APIView):
    def delete(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response('Event deleted')

