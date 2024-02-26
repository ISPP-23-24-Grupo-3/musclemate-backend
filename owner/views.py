from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Owner
from .serializers import OwnerSerializer



class OwnerListView(APIView):
    def get(self, request):
        owners = Owner.objects.all()
        serializer=OwnerSerializer(owners,many=True)
        return Response(serializer.data)
    
class OwnerDetailView(APIView):
    def get(self, request,pk):
        owner = Owner.objects.get(pk=pk)
        serializer=OwnerSerializer(owner)
        return Response(serializer.data)

class OwnerCreateView(APIView):
    def post(self, request):
        serializer = OwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class OwnerUpdateView(APIView):
    def post(self, request, pk):
        owner = Owner.objects.get(pk=pk)
        serializer = OwnerSerializer(owner, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class OwnerDeleteView(APIView):
    def delete(self, request, pk):
        owner = Owner.objects.get(pk=pk)
        owner.delete()
        return Response('Owner deleted')