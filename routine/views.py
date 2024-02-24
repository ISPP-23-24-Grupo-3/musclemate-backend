from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Routine
from .serializers import RoutineSerializer

class RoutineListView(APIView):
    def get(self, request):
        routines = Routine.objects.all()
        serializer = RoutineSerializer(routines, many=True)
        return Response(serializer.data)

class RoutineCreateView(APIView):
    def post(self, request):
        serializer = RoutineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoutineUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Routine.objects.get(pk=pk)
        except Routine.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        routine = self.get_object(pk)
        serializer = RoutineSerializer(routine, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoutineDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Routine.objects.get(pk=pk)
        except Routine.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        routine = self.get_object(pk)
        routine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



