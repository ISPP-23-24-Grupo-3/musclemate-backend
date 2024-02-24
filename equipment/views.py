from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Equipment
from .serializers import EquipmentSerializer

class EquipmentList(APIView):
    def get(self, request):
        equipments = Equipment.objects.all()
        serializer = EquipmentSerializer(equipments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EquipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EquipmentDetail(APIView):
    def get_object(self, id):
        try:
            return Equipment.objects.get(id=id)
        except Equipment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        equipment = self.get_object(id)
        serializer = EquipmentSerializer(equipment)
        return Response(serializer.data)

    def put(self, request, id):
        equipment = self.get_object(id)
        serializer = EquipmentSerializer(equipment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        equipment = self.get_object(id)
        equipment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


