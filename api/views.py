from django.shortcuts import render
from .models import Gym
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

@api_view(['GET'])
def gym_list(request):
    gyms = Gym.objects.all()
    data = {'gyms': list(gyms.values())}
    return Response(data)

@api_view(['GET'])
def gym_detail(request, id):
    gym = get_object_or_404(Gym, id=id)
    data = {'gym': model_to_dict(gym)}
    return Response(data)

@api_view(['DELETE'])
def gym_delete(request, id):
    gym = get_object_or_404(Gym, id=id)
    if request.method == 'DELETE':
        gym.delete()
        return Response({'message': 'Gym deleted successfully'})
    else:
        return Response({'error': 'DELETE method required'}, status=400)
