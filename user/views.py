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
    permission_classes = [IsAuthenticated]  # Add this line

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

class UserCreateView(APIView):

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class UserUpdateView(APIView):
    def post(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class UserDeleteView(APIView):
    def delete(self, request, pk):
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

