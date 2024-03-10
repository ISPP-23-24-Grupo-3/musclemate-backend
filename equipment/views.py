from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import IsGymOwner
from .models import Equipment
from workout.models import Workout
from serie.models import Serie
from owner.models import Owner
from gym.models import Gym
from client.models import Client
from .serializers import EquipmentSerializer

def isAllowed(equipment, user):
    if user.rol == "client":
        return get_object_or_404(Client, user=user).gym == equipment.gym
    elif user.rol == "gym":
        return get_object_or_404(Gym, userCustom=user) == equipment.gym
    elif user.rol == "owner":
        return get_object_or_404(Owner, userCustom=user) == equipment.gym.owner
    else:
        return True

@permission_classes([IsAuthenticated])
class EquipmentListView(APIView):
    def get(self, request):
        equipments = Equipment.objects.all()
        equipRet = []
        for equipment in equipments:
            if isAllowed(equipment, request.user):
                equipRet.append(equipment)
        serializer = EquipmentSerializer(equipRet, many=True)
        return Response(serializer.data)

@permission_classes([IsAuthenticated])
class EquipmentDetailView(APIView):
    def get(self, request, pk):
        equipment = Equipment.objects.get(pk=pk)
        if isAllowed(equipment, request.user):
            serializer=EquipmentSerializer(equipment)
            return Response(serializer.data)
        else:
            return Response({'message': "Please authenticate as the provided gym's owner, client or gym user"}, status=401)

@permission_classes([IsAuthenticated, IsGymOwner])
class EquipmentCreateView(APIView):
    def post(self, request):
        owner = get_object_or_404(Owner, userCustom=request.user)
        gym = get_object_or_404(Gym, id=request.data.get("gym"))
        if gym.owner == owner:
            serializer = EquipmentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': "Please authenticate as the provided gym's owner"}, status=401)

@permission_classes([IsAuthenticated, IsGymOwner])
class EquipmentUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        equipment = self.get_object(pk)
        owner = get_object_or_404(Owner, userCustom=request.user)
        gym = get_object_or_404(Gym, id=equipment.gym)
        if gym.owner == owner:
            serializer = EquipmentSerializer(equipment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': "Please authenticate as the provided gym's owner"}, status=401)

@permission_classes([IsAuthenticated, IsGymOwner])
class EquipmentDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        equipment = self.get_object(pk)
        owner = get_object_or_404(Owner, userCustom=request.user)
        gym = get_object_or_404(Gym, id=equipment.gym)
        if gym.owner == owner:
            equipment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': "Please authenticate as the provided gym's owner"}, status=401)

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