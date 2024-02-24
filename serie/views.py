from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Serie



class SerieListView(APIView):
    def get(self, request):
        series = Serie.objects.all()
        return Response(series.data)
    
class SerieDetailView(APIView):
    def get(self, request,pk):
        serie = Serie.objects.get(pk=pk)
        if serie:
            return Response({serie.data})
        else:
            return Response({"error": "Serie not found"}, status=status.HTTP_404_NOT_FOUND)

class SerieCreateView(APIView):
    def post(self, request):
        serie= Serie(**request.data)
        serie.save()
        return Response(serie.data)


class SerieUpdateView(APIView):
    def post(self, request, pk):
        serie = Serie.objects.get(pk=pk)
        serie=serie.__dict__.update(request.data)
        serie.save()
        return Response(serie.data)

class SerieDeleteView(APIView):
    def delete(self, request, pk):
        serie = Serie.objects.get(pk=pk)
        serie.delete()
        return Response('Serie deleted')