from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Workout
from .serializers import WorkoutSerializer

class WorkoutListView(APIView):
    def get(self, request):
        workouts = Workout.objects.all()
        serializer=WorkoutSerializer(workouts,many=True)
        return Response(serializer.data)
    
class WorkoutDetailView(APIView):
    def get(self, request,pk):
        workout = Workout.objects.get(pk=pk)
        serializer=WorkoutSerializer(workout)
        return Response(serializer.data)

class WorkoutCreateView(APIView):
    def post(self, request):
        serializer = WorkoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class WorkoutUpdateView(APIView):
    def post(self, request, pk):
        workout = Workout.objects.get(pk=pk)
        serializer = WorkoutSerializer(workout, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class WorkoutDeleteView(APIView):
    def delete(self, request, pk):
        workout = Workout.objects.get(pk=pk)
        workout.delete()
        return Response('Workout deleted')
