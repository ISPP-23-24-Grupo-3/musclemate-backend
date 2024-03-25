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
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsGymOwner])
def subscription_standar_uptade(request, gym_id):
    gym = get_object_or_404(Gym, id=gym_id)
    owner = get_object_or_404(Owner, userCustom=request.user)
    if gym.owner == owner:
        if request.method == 'PUT':
            gym_data = request.data
            gym_data['subscription_plan'] = 'standard'
            serializer = GymSerializer(gym, data=gym_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                gym.refresh_from_db()
                return Response({'message': 'Subscription plan updated to standard'})
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({'error': 'PUT method required'}, status=400)
    else:
        return Response({'message': "Please authenticate as this gym's owner"}, status=401)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsGymOwner])
def subscription_premium_uptade(request, gym_id):
    gym = get_object_or_404(Gym, id=gym_id)
    owner = get_object_or_404(Owner, userCustom=request.user)
    if gym.owner == owner:
        if request.method == 'PUT':
            gym_data = request.data
            gym_data['subscription_plan'] = 'premium'
            serializer = GymSerializer(gym, data=gym_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Subscription plan updated to premium'})
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({'error': 'PUT method required'}, status=400)
    else:
        return Response({'message': "Please authenticate as this gym's owner"}, status=401)