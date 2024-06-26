from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import CustomUser
from .models import Routine,Client
from .serializers import RoutineSerializer, RoutineCreateSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@permission_classes([IsAuthenticated])
class RoutineListView(APIView):
    def get(self, request):
        if request.user.rol=='client':
            user = CustomUser.objects.get(username=request.user)
            client = Client.objects.get(user=user)
            routines = Routine.objects.filter(client=client)
            serializer = RoutineSerializer(routines, many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)

@permission_classes([IsAuthenticated])
class RoutineDetailView(APIView):
    def get(self, request,pk):
        if request.user.rol=='client':
            clientIdByUser=Client.objects.get(user=request.user).id
            clientIdByRoutine=Routine.objects.get(pk=pk).client.id
            if clientIdByRoutine==clientIdByUser:
                routine = Routine.objects.get(pk=pk)
                serializer = RoutineSerializer(routine)
                return Response(serializer.data)
            else:
                return Response(status=403)
        else:
            return Response(status=403)

@permission_classes([IsAuthenticated])
class RoutineCreateView(APIView):
    def post(self, request):
        if request.user.rol=='client':
            clientIdByUser = Client.objects.get(user=request.user)
            serializer = RoutineCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(client=clientIdByUser)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=403)

@permission_classes([IsAuthenticated])
class RoutineUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Routine.objects.get(pk=pk)
        except Routine.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        if request.user.rol=='client':
            clientIdByUser=Client.objects.get(user=request.user).id
            clientIdByRoutine=Routine.objects.get(pk=pk).client.id
            if clientIdByRoutine==clientIdByUser:
                routine = self.get_object(pk)
                serializer = RoutineSerializer(routine, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=403)
        else:
            return Response(status=403)

@permission_classes([IsAuthenticated])
class RoutineDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Routine.objects.get(pk=pk)
        except Routine.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if request.user.rol=='client':
            clientIdByUser=Client.objects.get(user=request.user).id
            clientIdByRoutine=Routine.objects.get(pk=pk).client.id
            if clientIdByRoutine==clientIdByUser:
                routine = self.get_object(pk)
                routine.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=403)
        else:
            return Response(status=403)