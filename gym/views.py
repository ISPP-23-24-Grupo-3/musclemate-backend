from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Gym
from .serializers import GymSerializer

@api_view(['GET'])
def gym_list(request):
    gyms = Gym.objects.all()
    serializer = GymSerializer(gyms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def gym_detail(request, id):
    gym = get_object_or_404(Gym, id=id)
    serializer = GymSerializer(gym)
    return Response(serializer.data)

@api_view(['POST'])
def gym_create(request):
    if request.method == 'POST':
        serializer = GymSerializer(data=request.data)
        if serializer.is_valid():
            gym = serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['PUT'])
def gym_update(request, id):
    gym = get_object_or_404(Gym, id=id)
    if request.method == 'PUT':
        serializer = GymSerializer(gym, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def gym_delete(request, id):
    gym = get_object_or_404(Gym, id=id)
    if request.method == 'DELETE':
        gym.delete()
        return Response({'message': 'Gym deleted successfully'})
    else:
        return Response({'error': 'DELETE method required'}, status=400)