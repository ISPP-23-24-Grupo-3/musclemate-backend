from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import IsGymOwner
from django.shortcuts import get_object_or_404
from .models import Gym
from owner.models import Owner
from client.models import Client
from .serializers import GymSerializer
from user.serializers import CustomUserSerializer
from owner.models import Owner
from django.db.models import Count
from serie.models import Serie
from datetime import datetime
from django.http import JsonResponse


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
@permission_classes([IsAuthenticated])
def gym_detail(request, id):
    gym = get_object_or_404(Gym, id=id)
    if (request.user.rol == "owner"):
        owner = get_object_or_404(Owner, userCustom=request.user)
        if gym.owner == owner:
            serializer = GymSerializer(gym)
            return Response(serializer.data)
        else:
            return Response({'message': "Por favor inicie sesión como el dueño de este gimnasio"}, status=401)
    if (request.user.rol == 'client'):
        client = get_object_or_404(Client, user=request.user)
        if client.gym.id == id:
            serializer = GymSerializer(gym)
            return Response(serializer.data)
        else:
            return Response({'message': "Por favor inicie sesión como el cliente de este gimnasio"}, status=401)
    if (request.user.rol == 'gym'):
        gymreq = get_object_or_404(Gym, userCustom=request.user)
        if gym == gymreq:
            serializer = GymSerializer(gym)
            return Response(serializer.data)
        else:
            return Response({'message': "Por favor inicie sesión como este gimnasio"}, status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gym_detail_username(request, username):
    gym = get_object_or_404(Gym, userCustom=username)
    if (request.user.rol == "owner"):
        owner = get_object_or_404(Owner, userCustom=request.user)
        if gym.owner == owner:
            serializer = GymSerializer(gym)
            return Response(serializer.data)
        else:
            return Response({'message': "Por favor inicie sesión como el dueño de este gimnasio"}, status=401)
    if (request.user.rol == 'gym'):
        gymreq = get_object_or_404(Gym, userCustom=request.user)
        if gym == gymreq:
            serializer = GymSerializer(gym)
            return Response(serializer.data)
        else:
            return Response({'message': "Por favor inicie sesión como este gimnasio"}, status=401)

@api_view(['POST'])
def gym_create(request):
    if request.method == 'POST':
        if request.user.rol != 'owner':
            return Response('No tiene la autorización para crear un gimnasio', status=403)
        user_data = request.data.get('userCustom')
        user_data['email'] = request.data.get('email')
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
                user.delete()
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
            serializer = GymSerializer(gym, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        else:
            return Response({'error': 'PUT method required'}, status=400)
    else:
        return Response({'message': "Por favor inicie sesión como el dueño de este gimnasio"}, status=401)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsGymOwner])
def gym_delete(request, id):
    gym = get_object_or_404(Gym, id=id)
    owner = get_object_or_404(Owner, userCustom=request.user)
    if gym.owner == owner:
        if request.method == 'DELETE':
            gym.delete()
            return Response({'message': 'Gimnasio eliminado correctamente'})
        else:
            return Response({'error': 'DELETE method required'}, status=400)
    else:
        return Response({'message': "Por favor inicie sesión como el dueño de este gimnasio"}, status=401)

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
                return Response({'message': 'Plan de subscripción actualizado a standard'})
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({'error': 'PUT method required'}, status=400)
    else:
        return Response({'message': "Por favor inicie sesión como el dueño de este gimnasio"}, status=401)

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
                return Response({'message': 'Plan de subscripción actualizado a premium'})
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({'error': 'PUT method required'}, status=400)
    else:
        return Response({'message': "Por favor inicie sesión como el dueño de este gimnasio"}, status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsGymOwner])
def monthly_usage(request, gym_id, year=None, month=None):
    gym = get_object_or_404(Gym, id=gym_id)
    owner = get_object_or_404(Owner, userCustom=request.user)
    if year is None:
        current_year = datetime.now().year
    else:
        current_year = year
    if month is None:
        current_month = datetime.now().month
    else:
        current_month = month
    print(year, month)
    print(current_year, current_month)
    if gym.owner == owner:
        if request.method == 'GET':
            if year is not None and month is None:
                data = Serie.objects.filter(
                    date__year=current_year)\
                    .values('workout__equipment__name', 'date__month')\
                    .annotate(total=Count('workout__equipment__name'))
            else:
                print(current_year, current_month)
                data = Serie.objects.filter(
                    workout__client__gym=gym,
                    date__year=current_year,
                    date__month=current_month)\
                    .values('workout__equipment__name')\
                    .annotate(total=Count('workout__equipment__name'))
            formatted_data = []
            for entry in data:
                formatted_data.append({
                    'month': entry['date__month'] if 'date__month' in entry else current_month,
                    'equipment_name': entry['workout__equipment__name'],
                    'total': entry['total']
                })
            return JsonResponse(formatted_data, safe=False)
        else:
            return Response({'error': 'GET method required'}, status=400)
    else:
        return Response({'message': "Por favor inicie sesión como el dueño de este gimnasio"}, status=401)
