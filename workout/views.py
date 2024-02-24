from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Workout



class WorkoutListView(APIView):
    def get(self, request):
        workouts = Workout.objects.all()
        return Response(workouts.data)
    
class WorkoutDetailView(APIView):
    def get(self, request,pk):
        workout = Workout.objects.get(pk=pk)
        if workout:
            return Response({workout.data})
        else:
            return Response({"error": "Workout not found"}, status=status.HTTP_404_NOT_FOUND)

class WorkoutCreateView(APIView):
    def post(self, request):
        workout= Workout(**request.data)
        workout.save()
        return Response(workout.data)


class WorkoutUpdateView(APIView):
    def post(self, request, pk):
        workout = Workout.objects.get(pk=pk)
        workout=workout.__dict__.update(request.data)
        workout.save()
        return Response(workout.data)

class WorkoutDeleteView(APIView):
    def delete(self, request, pk):
        workout = Workout.objects.get(pk=pk)
        workout.delete()
        return Response('Workout deleted')
