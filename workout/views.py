from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import WorkoutSerializer, WorkoutCreateSerializer
from .models import Workout, Client, Equipment, Routine
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

class WorkoutListView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            workouts = Workout.objects.filter(client__user=request.user)
        if request.user.is_superuser:
            workouts = Workout.objects.all()
        serializer=WorkoutSerializer(workouts,many=True)
        return Response(serializer.data)
    
class WorkoutDetailView(APIView):
    def get(self, request,pk):
        workout = Workout.objects.get(pk=pk)
        if request.user != workout.client.user:
            return Response({'message': 'You are not allowed to see this workout'}, status=401)
        serializer=WorkoutSerializer(workout)
        return Response(serializer.data)

@permission_classes([IsAuthenticated])
class WorkoutCreateView(APIView):
    def post(self, request):
        if request.user.rol == "client":
            serializer = WorkoutCreateSerializer(data=request.data)
            client = Client.objects.get(user=request.user.username)
            if serializer.is_valid():
                has_equipment = 'equipment' in serializer.validated_data
                has_routine = 'routine' in serializer.validated_data

                if has_equipment or has_routine:
                    # Convert ManyRelatedManager to list for iteration
                    equipment_ids = [eq.id for eq in serializer.validated_data.get('equipment', [])]
                    routine_ids = [rt.id for rt in serializer.validated_data.get('routine', [])]
                    
                    for equipment_id in equipment_ids:
                        equipment_exists = Equipment.objects.filter(id=equipment_id).exists()

                        if equipment_exists:
                            equipment = Equipment.objects.get(id=equipment_id)
                            if client.gym != equipment.gym:
                                return Response({'message': 'You are not allowed to create a workout with this equipment or routine'}, status=401)

                    for routine_id in routine_ids:
                        routine_exists = Routine.objects.filter(id=routine_id).exists()

                        if routine_exists:
                            routine = Routine.objects.get(id=routine_id)
                            if client != routine.client:
                                return Response({'message': 'You are not allowed to create a workout with this equipment or routine'}, status=401)

                    serializer.save()
                    return Response(serializer.data, status=201)

                else:
                    # Handle case when both equipment and routine are empty
                    serializer.save()
                    return Response(serializer.data, status=201)

            else:
                return Response(serializer.errors, status=400)
        
        else:
            Response(status=403)

class WorkoutUpdateView(APIView):
    def put(self, request, pk):
        workout = Workout.objects.get(pk=pk)
        serializer = WorkoutCreateSerializer(workout, data=request.data)
        if serializer.is_valid():
            if request.user == workout.client.user:
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'message': 'You are not allowed to update this workout'}, status=401)
        return Response(serializer.errors, status=400)

class WorkoutDeleteView(APIView):
    def delete(self, request, pk):
        workout = Workout.objects.get(pk=pk)
        if request.user == workout.client.user:
            workout.delete()
        else:
            return Response({'message': 'You are not allowed to delete this workout'}, status=401)
        return Response('Workout deleted')
