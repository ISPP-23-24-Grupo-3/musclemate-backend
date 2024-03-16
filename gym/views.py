from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import IsGymOwner
from django.shortcuts import get_object_or_404
from .models import Gym
from owner.models import Owner
from .serializers import GymSerializer
from user.serializers import CustomUserSerializer
from user.models import CustomUser
from owner.models import Owner


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsGymOwner])
def gym_list(request):
    gyms = Gym.objects.all()
    owner = get_object_or_404(Owner, userCustom=request.user)
    gymsRet = []
    for gym in gyms:
        if gym.owner == owner: gymsRet.append(gym)
    serializer = GymSerializer(gymsRet, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsGymOwner])
def gym_detail(request, id):
    gym = get_object_or_404(Gym, id=id)
    owner = get_object_or_404(Owner, userCustom=request.user)
    if gym.owner == owner:
        serializer = GymSerializer(gym)
        return Response(serializer.data)
    else:
        return Response({'message': "Please authenticate as this gym's owner"}, status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsGymOwner])
def gym_create(request):
    if request.method == 'POST':
        user_serializer = CustomUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save(rol='gym')
            gym_data = request.data.dict()
            gym_data['userCustom'] = user.username
            gym_serializer = GymSerializer(data=gym_data)
            if gym_serializer.is_valid():
                gym_serializer.save()
                return Response(gym_serializer.data, status=201)
            else:
                return Response(gym_serializer.errors, status=400)
        else:
            return Response(user_serializer.errors, status=400)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsGymOwner])
def gym_update(request, id):
    gym = get_object_or_404(Gym, id=id)
    owner = get_object_or_404(Owner, userCustom=request.user)
    if gym.owner == owner:
        if request.method == 'PUT':
            serializer = GymSerializer(gym, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        else:
            return Response({'error': 'PUT method required'}, status=400)
    else:
        return Response({'message': "Please authenticate as this gym's owner"}, status=401)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsGymOwner])
def gym_delete(request, id):
    gym = get_object_or_404(Gym, id=id)
    owner = get_object_or_404(Owner, userCustom=request.user)
    if gym.owner == owner:
        if request.method == 'DELETE':
            gym.delete()
            return Response({'message': 'Gym deleted successfully'})
        else:
            return Response({'error': 'DELETE method required'}, status=400)
    else:
        return Response({'message': "Please authenticate as this gym's owner"}, status=401)