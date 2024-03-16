from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Workout, Client, Equipment, Routine
from .serializers import WorkoutSerializer

class WorkoutListView(APIView):
    def get(self, request):
        workouts = Workout.objects.none()
        if request.user.is_superuser:
            workouts = Workout.objects.all()  # Establece un queryset vacío como valor inicial
        elif request.user.is_authenticated:
            workouts = Workout.objects.filter(client__user=request.user)
        
        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data)
    
class WorkoutDetailView(APIView):
    def get(self, request,pk):
        workout = Workout.objects.get(pk=pk)
        if request.user != workout.client.user:
            return Response({'message': 'You are not allowed to see this workout'}, status=401)
        serializer=WorkoutSerializer(workout)
        return Response(serializer.data)


class WorkoutCreateView(APIView):
    def post(self, request):
        serializer = WorkoutSerializer(data=request.data)
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
                            print("Equipment check failed")
                            return Response({'message': 'You are not allowed to create a workout with this equipment or routine'}, status=401)

                for routine_id in routine_ids:
                    routine_exists = Routine.objects.filter(id=routine_id).exists()

                    if routine_exists:
                        routine = Routine.objects.get(id=routine_id)
                        if client != routine.client:
                            print("Routine check failed")
                            return Response({'message': 'You are not allowed to create a workout with this equipment or routine'}, status=401)

                serializer.save()
                print("Workout created successfully")
                return Response(serializer.data, status=201)

            else:
                # Handle case when both equipment and routine are empty
                serializer.save()
                print("Workout created successfully with no equipment or routine")
                return Response(serializer.data, status=201)

        else:
            print("Validation failed")
            return Response(serializer.errors, status=400)




class WorkoutUpdateView(APIView):
    def post(self, request, pk):
        workout = Workout.objects.get(pk=pk)
        serializer = WorkoutSerializer(workout, data=request.data)
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
