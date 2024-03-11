from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Serie
from .models import Workout
from client.models import Client
from .serializers import SerieSerializer
from rest_framework.permissions import BasePermission


class IsGymOrOwner(BasePermission):
    def has_permission(self,request):
        return request.user.is_authenticated and (request.user.rol == 'gym' or request.user.rol == 'owner')

class SerieListView(APIView):
    def get(self, request):
        if IsGymOrOwner().has_permission(request):
            series = Serie.objects.all()
            serializer=SerieSerializer(series,many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)

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





class SerieCreateView(APIView):
    def post(self, request):
        serializer = SerieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
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


class SerieUpdateView(APIView):
    def post(self, request, pk):
        if request.user.rol == 'client':
            clientIdByUser=Client.objects.get(user=request.user).id
            serie = Serie.objects.get(pk=pk)
            clientIdBySerie=serie.workout.client.id
            if clientIdByUser==clientIdBySerie:
                serializer = SerieSerializer(serie, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
            else:
                return Response('clientId diferent of workoutClientId',status=403)
        else:
            return Response('rol is not Client',status=403)



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