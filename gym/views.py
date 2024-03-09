from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Gym
from .serializers import GymSerializer
from user.serializers import CustomUserSerializer
from user.models import CustomUser
from owner.models import Owner


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
        if request.user.rol != 'admin' and request.user.rol != 'owner':
            return Response('You are not authorized to create a gym')
        user_data = request.data.get('userCustom')
        user_serializer = CustomUserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save(rol='gym')
            gym_data = request.data
            gym_data['userCustom'] = user.username
            owner = Owner.objects.get(userCustom=request.user.username)
            gym_data['owner'] = owner.id
            gym_serializer = GymSerializer(data=gym_data)
            if gym_serializer.is_valid():
                gym_serializer.save()
                return Response(gym_serializer.data, status=201)
            else:
                return Response(gym_serializer.errors, status=400)
        else:
            return Response(user_serializer.errors, status=400)

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