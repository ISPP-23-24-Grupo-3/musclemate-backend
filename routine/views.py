from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Routine,Client
from .serializers import RoutineSerializer

class RoutineListView(APIView):
    def get(self, request):
        if request.user.rol=='gym' or request.user.rol=='owner':
            routines = Routine.objects.all()
            serializer = RoutineSerializer(routines, many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)
    
class RoutineListByClientView(APIView):
    def get(self, request,clientId):
        clientIdByUser=Client.objects.get(user=request.user).id
        if request.user.rol=='gym' or request.user.rol=='owner' or clientId==clientIdByUser:
            routines = Routine.objects.filter(client=clientId)
            serializer = RoutineSerializer(routines, many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)
    
class RoutineDetailView(APIView):
    def get(self, request,pk):
        clientIdByUser=Client.objects.get(user=request.user).id
        clientIdByRoutine=Routine.objects.get(pk=pk).client.id
        if clientIdByRoutine==clientIdByUser:
            routine = Routine.objects.get(pk=pk)
            serializer = RoutineSerializer(routine)
            return Response(serializer.data)
        else:
            return Response(status=403)

class RoutineCreateView(APIView):
    def post(self, request):
        clientIdByUser=Client.objects.get(user=request.user).id
        if request.user.rol=='client' and request.data.get('client')==clientIdByUser:
            serializer = RoutineSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=403)

class RoutineUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Routine.objects.get(pk=pk)
        except Routine.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        clientIdByUser=Client.objects.get(user=request.user).id
        clientIdByRoutine=Routine.objects.get(pk=pk).client.id
        if clientIdByRoutine==clientIdByUser:
            routine = self.get_object(pk)
            serializer = RoutineSerializer(routine, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=403)

class RoutineDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Routine.objects.get(pk=pk)
        except Routine.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        clientIdByUser=Client.objects.get(user=request.user).id
        clientIdByRoutine=Routine.objects.get(pk=pk).client.id
        if clientIdByRoutine==clientIdByUser:
            routine = self.get_object(pk)
            routine.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=403)



