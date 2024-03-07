from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Serie
from .serializers import SerieSerializer



class SerieListView(APIView):
    def get(self, request):
        series = Serie.objects.all()
        serializer=SerieSerializer(series,many=True)
        return Response(serializer.data)
    
class SerieDetailView(APIView):
    def get(self, request,pk):
        serie = Serie.objects.get(pk=pk)
        serializer=SerieSerializer(serie)
        return Response(serializer.data)

class SerieCreateView(APIView):
    def post(self, request):
        serializer = SerieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class SerieUpdateView(APIView):
    def post(self, request, pk):
        serie = Serie.objects.get(pk=pk)
        serializer = SerieSerializer(serie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class SerieDeleteView(APIView):
    def delete(self, request, pk):
        serie = Serie.objects.get(pk=pk)
        serie.delete()
        return Response('Serie deleted')