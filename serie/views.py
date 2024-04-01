from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Serie
from .models import Workout
from client.models import Client
from .serializers import SerieSerializer
from rest_framework.permissions import BasePermission
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

class IsGymOrOwner(BasePermission):
    def has_permission(self,request):
        return request.user.is_authenticated and (request.user.rol == 'gym' or request.user.rol == 'owner')

class SerieListView(APIView):
    def get(self, request):
        if request.user.rol == 'client':
            series = Serie.objects.all()
            serializer=SerieSerializer(series,many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)

@permission_classes([IsAuthenticated])
class SerieListByWorkoutView(APIView):
    def get(self, request,pk):
        if request.user.rol == 'client':
            clientIdByUser=Client.objects.get(user=request.user).id
            workout = Workout.objects.get(pk=pk)
            clientIdByWorkout=workout.client.id
            if clientIdByUser == clientIdByWorkout:
                series = Serie.objects.filter(workout=pk)
                serializer=SerieSerializer(series,many=True)
                return Response(serializer.data)
            else:
                return Response(status=403)
        else:
            return Response(status=403)

@permission_classes([IsAuthenticated])
class SerieDetailView(APIView):
    def get(self, request,pk):
        if request.user.rol == 'client':
            clientIdByUser = Client.objects.get(user=request.user).id
            serie = Serie.objects.get(pk=pk)
            clientIdBySerie = serie.workout.client.id
            if clientIdByUser == clientIdBySerie:
                serializer = SerieSerializer(serie)
                return Response(serializer.data)
            else:
                return Response(status=403)
        else:
            return Response(status=403)
@permission_classes([IsAuthenticated])
class SerieCreateView(APIView):
    def post(self, request):
        if request.user.rol == "client":
            clientIdByWorkout=Workout.objects.get(pk=request.data.get('workout')).client.id
            clientIdByUser=Client.objects.get(user=request.user).id
            if clientIdByUser == clientIdByWorkout:
                serializer = SerieSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=201)
                else:
                    return Response(serializer.errors, status=400)
            else:
                return Response(status=403)
        else:
            return Response(status=403)
@permission_classes([IsAuthenticated])
class SerieUpdateView(APIView):
    def put(self, request, pk):
        if request.user.rol == 'client':
            clientIdByUser=Client.objects.get(user=request.user).id
            serie = Serie.objects.get(pk=pk)
            clientIdBySerie=serie.workout.client.id
            if clientIdByUser==clientIdBySerie:
                serializer = SerieSerializer(serie, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
            else:
                return Response('clientId diferent of workoutClientId',status=403)
        else:
            return Response('rol is not Client',status=403)
@permission_classes([IsAuthenticated])
class SerieDeleteView(APIView):
    def delete(self, request, pk):
        if request.user.rol == 'client':
            clientIdByUser=Client.objects.get(user=request.user).id
            serie = Serie.objects.get(pk=pk)
            clientIdBySerie=serie.workout.client.id
            if clientIdByUser==clientIdBySerie:
                serie.delete()
                return Response('Serie deleted')
            else:
                return Response('clientId diferent of workoutClientId',status=403)
        else:
            return Response('rol is not Client',status=403)