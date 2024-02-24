from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Owner



class OwnerListView(APIView):
    def get(self, request):
        owners = Owner.objects.all()
        return Response(owners.data)
    
class OwnerDetailView(APIView):
    def get(self, request,pk):
        owner = Owner.objects.get(pk=pk)
        if owner:
            return Response({owner.data})
        else:
            return Response({"error": "Owner not found"}, status=status.HTTP_404_NOT_FOUND)

class OwnerCreateView(APIView):
    def post(self, request):
        owner= Owner(**request.data)
        owner.save()
        return Response(owner.data)


class OwnerUpdateView(APIView):
    def post(self, request, pk):
        owner = Owner.objects.get(pk=pk)
        owner=owner.__dict__.update(request.data)
        owner.save()
        return Response(owner.data)

class OwnerDeleteView(APIView):
    def delete(self, request, pk):
        owner = Owner.objects.get(pk=pk)
        owner.delete()
        return Response('Owner deleted')