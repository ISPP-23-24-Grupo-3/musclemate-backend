from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
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
            return Response({'message': "Por favor inicie sesión como el dueño de, cliente de o el gimnasio indicado"}, status=401)

@permission_classes([IsAuthenticated])
class EquipmentCreateView(APIView):
    def post(self, request):
        gym = get_object_or_404(Gym, id=request.data.get("gym"))
        if request.user.rol == "owner":
            owner = get_object_or_404(Owner, userCustom=request.user)
            if gym.owner == owner:
                serializer = EquipmentSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': "Por favor inicie sesión como el dueño de el gimnasio indicado"}, status=401)
        elif request.user.rol == "gym":
            if gym.userCustom == request.user:
                serializer = EquipmentSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': "Por favor inicie sesión como el gimnasio indicado"}, status=401)

@permission_classes([IsAuthenticated])
class EquipmentUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        equipment = self.get_object(pk)
        gym = get_object_or_404(Gym, id=equipment.gym.id)
        if request.user.rol == "owner":
            owner = get_object_or_404(Owner, userCustom=request.user)
            if gym.owner == owner:
                serializer = EquipmentSerializer(equipment, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': "Por favor inicie sesión como el dueño de el gimnasio indicado"}, status=401)
        elif request.user.rol == "gym":
            if gym.userCustom == request.user:
                serializer = EquipmentSerializer(equipment, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': "Por favor inicie sesión como el gimnasio indicado"}, status=401)

@permission_classes([IsAuthenticated])
class EquipmentDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        equipment = self.get_object(pk)
        gym = get_object_or_404(Gym, id=equipment.gym.id)
        if request.user.rol == "owner":
            owner = get_object_or_404(Owner, userCustom=request.user)
            if gym.owner == owner:
                equipment.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': "Por favor inicie sesión como el dueño de el gimnasio indicado"}, status=401)
        elif request.user.rol == "gym":
            if gym.userCustom == request.user:
                equipment.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': "Por favor inicie sesión como el gimnasio indicado"}, status=401)

class EquipmentObtainTime(APIView):
    def get_object(self, pk):
        try:
            return Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        equipment = self.get_object(pk)
        owner = get_object_or_404(Owner, userCustom=request.user)
        gym = get_object_or_404(Gym, id=equipment.gym.id)
        if gym.owner == owner:
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
        else:
            return Response({'message': "Por favor inicie sesión como el dueño de el gimnasio indicado"}, status=401)

class EquipmentGlobalList(APIView):
    """ permission_classes = [IsAuthenticated] """

    def get(self, request):
        owner = Owner.objects.get(userCustom=request.user)
        gyms = Gym.objects.filter(owner=owner, subscription_plan="premium")
        if request.user.rol == "owner" and gyms.count() > 0:
            workouts = Workout.objects.all()
            equipment_count = {}
            for workout in workouts:
                for equipment in workout.equipment.all():
                    if equipment in equipment_count:
                        equipment_count[equipment] += 1
                    else:
                        equipment_count[equipment] = 1
            sorted_equipment = sorted(equipment_count.items(), key=lambda x: x[1], reverse=True)
            equipment_list = [item[0] for item in sorted_equipment]
            serializer = EquipmentSerializer(equipment_list, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': "Acceso no autorizado"}, status=401)