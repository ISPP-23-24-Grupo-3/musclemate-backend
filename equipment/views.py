from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Equipment
from workout.models import Workout
from serie.models import Serie
from .serializers import EquipmentSerializer

class EquipmentListView(APIView):
    def get(self, request):
        equipments = Equipment.objects.all()
        serializer = EquipmentSerializer(equipments, many=True)
        return Response(serializer.data)

class EquipmentDetailView(APIView):
    def get(self, request,pk):
        reservation = Equipment.objects.get(pk=pk)
        serializer=EquipmentSerializer(reservation)
        return Response(serializer.data)

class EquipmentCreateView(APIView):
    def post(self, request):
        serializer = EquipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EquipmentUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        equipment = self.get_object(pk)
        serializer = EquipmentSerializer(equipment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EquipmentDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        equipment = self.get_object(pk)
        equipment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EquipmentObtainTime(APIView):
    def get(self, request, pk):
        equipment = Equipment.objects.get(pk=pk)
        workouts = []
        timer = 0
        for workout in Workout.objects.all():
            if equipment in workout.equipment.all():
                workouts.append(workout)
        for serie in Serie.objects.all():
            if serie.workout in workouts:
                timer += serie.duration
        return Response({"time": timer}, status=status.HTTP_200_OK)