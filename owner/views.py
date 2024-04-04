from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Owner, CustomUser
from gym.models import Gym
from .serializers import OwnerSerializer, CustomUserSerializer
from user.utils import send_verification_email



class OwnerListView(APIView):
    def get(self, request):
        if request.user.is_superuser:
            owners = Owner.objects.all()
        if request.user.rol=='gym':
            owners = Owner.objects.filter(gym__userCustom=request.user)
        serializer=OwnerSerializer(owners,many=True)
        return Response(serializer.data)
    
class OwnerDetailView(APIView):
    def get(self, request,pk):
        if (request.user.rol=='owner' and request.user.username==pk) or request.user.is_superuser:
            owner = Owner.objects.get(userCustom=pk)
            serializer=OwnerSerializer(owner)
            return Response(serializer.data)
        elif request.user.rol=='gym':
            gym = Gym.objects.get(userCustom=request.user)
            if gym.owner.userCustom.username==pk:
                owner = Owner.objects.get(userCustom=pk)
                serializer=OwnerSerializer(owner)
                return Response(serializer.data)
            else:
                return Response('You are not authorized to see this owner',status=403)
        else:
            return Response('You are not authorized to see this owner',status=403)

class OwnerCreateView(APIView):
    def post(self, request):
        user_data = request.data.get('userCustom')
        user_data['email'] = request.data.get('email')
        user_serializer = CustomUserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save(rol='owner')
            owner_data = request.data
            owner_data['userCustom'] = user.username
            owner_serializer = OwnerSerializer(data=owner_data)
            if owner_serializer.is_valid():
                owner_serializer.save()
                try:
                    send_verification_email(user)
                except:
                    return Response("Owner registered but e-mail verification failed.", status=201)
                else:
                    return Response(owner_serializer.data, status=201)
            else:
                user.delete()
                return Response(owner_serializer.errors, status=400)
        else:
            return Response(user_serializer.errors, status=400)

class OwnerUpdateView(APIView):
    def put(self, request, pk):
        if (request.user.rol=='owner' and request.user.username==pk) or request.user.is_superuser:
            owner = Owner.objects.get(userCustom=pk)
            serializer = OwnerSerializer(owner, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        elif request.user.rol=='gym':
            gym = Gym.objects.get(userCustom=request.user)
            if gym.owner.userCustom.username==pk:
                owner = Owner.objects.get(userCustom=pk)
                serializer = OwnerSerializer(owner, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
            else:
                return Response('You are not authorized to update a owner', status=403)
        else:
            return Response('You are not authorized to update a owner', status=403)

class OwnerDeleteView(APIView):
    def delete(self, request, pk):
        if request.user.is_superuser:
            owner = Owner.objects.get(pk=pk)
            user = CustomUser.objects.get(username=owner.userCustom)
            owner.delete()
            user.delete()
            return Response('Owner deleted')
        elif request.user.rol=='gym':
            owner = Owner.objects.get(pk=pk)
            gym = Gym.objects.get(userCustom=request.user)
            if gym.owner.userCustom.username==owner.userCustom.username:
                user = CustomUser.objects.get(username=owner.userCustom)
                owner.delete()
                user.delete()
                return Response('Owner deleted')
            else:
                return Response('You are not authorized to delete a owner', status=403)
        else:
            return Response('You are not authorized to delete a owner', status=403)
