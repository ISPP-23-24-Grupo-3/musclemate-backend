from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Owner, CustomUser
from .serializers import OwnerSerializer, CustomUserSerializer



class OwnerListView(APIView):
    def get(self, request):
        owners = Owner.objects.all()
        serializer=OwnerSerializer(owners,many=True)
        return Response(serializer.data)
    
class OwnerDetailView(APIView):
    def get(self, request,pk):
        owner = Owner.objects.get(userCustom = pk)
        serializer=OwnerSerializer(owner)
        return Response(serializer.data)

class OwnerCreateView(APIView):
    def post(self, request):
        user_data = request.data.get('userCustom')
        user_serializer = CustomUserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save(rol='owner')
            owner_data = request.data
            owner_data['userCustom'] = user.username
            owner_serializer = OwnerSerializer(data=owner_data)
            if owner_serializer.is_valid():
                owner_serializer.save()
                return Response(owner_serializer.data, status=201)
            else:
                return Response(owner_serializer.errors, status=400)
        else:
            return Response(user_serializer.errors, status=400)

class OwnerUpdateView(APIView):
    def put(self, request, pk):
        owner = Owner.objects.get(pk=pk)
        print(f"Request data: {request.data}")
        serializer = OwnerSerializer(owner, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print(f"Owner data after save: {serializer.data}")
            return Response(serializer.data)
        print(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=400)

class OwnerDeleteView(APIView):
    def delete(self, request, pk):
        owner = Owner.objects.get(pk=pk)
        user = CustomUser.objects.get(username=owner.userCustom)
        owner.delete()
        user.delete()
        return Response('Owner deleted')