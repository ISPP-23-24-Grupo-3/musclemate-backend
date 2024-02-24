from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Event



class EventListView(APIView):
    def get(self, request):
        events = Event.objects.all()
        return Response(events.data)
    
class EventDetailView(APIView):
    def get(self, request,pk):
        event = Event.objects.get(pk=pk)
        if event:
            return Response({event.data})
        else:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

class EventCreateView(APIView):
    def post(self, request):
        event= Event(**request.data)
        event.save()
        return Response(event.data)


class EventUpdateView(APIView):
    def post(self, request, pk):
        event = Event.objects.get(pk=pk)
        event=event.__dict__.update(request.data)
        event.save()
        return Response(event.data)

class EventDeleteView(APIView):
    def delete(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response('Event deleted')

