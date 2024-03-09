from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

class UserListView(APIView):
    def get(self, request):
        if request.user.rol != 'admin':
            return Response('You are not authorized to view this users')
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    
class UserDetailView(APIView):
    def get(self, request, username):
        if (request.user.username == username) or (request.user.rol == 'admin'):
            user = CustomUser.objects.get(username=username)
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response('You are not authorized to view this user')

class UserCreateView(APIView):
    def post(self, request):
        if request.user.rol != 'admin':
            return Response('You are not authorized to create a user')
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class UserUpdateView(APIView):
    def put(self, request, username):
        if request.user.rol != 'admin':
            return Response('You are not authorized to view this user')
        user = CustomUser.objects.get(username=username)
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
       

class UserDeleteView(APIView):
    def delete(self, request, pk):
        if request.user.rol != 'admin':
            return Response('You are not authorized to view this user')
        user = CustomUser.objects.get(pk=pk)
        user.delete()
        return Response('User deleted')
    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['rol'] = user.rol
        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    @api_view(['GET'])
    @permission_classes([IsAuthenticated]) 

    def get_routes(request):
        routes = [
            'api/token/',
            'api/token/refresh/',
            'api/users/',
            'api/users/create/',
            'api/users/update/<str:pk>/',
            'api/users/delete/<str:pk>/',
        ]
        return Response(routes)   

