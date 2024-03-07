from django.shortcuts import render
from .models import Assessment
from rest_framework.response import Response
from .serializers import AssessmentSerializer
from rest_framework import status
from rest_framework.views import APIView

class AssessmentListView(APIView):
    def get(self, request):
        assessments = Assessment.objects.all()
        serializer=AssessmentSerializer(assessments,many=True)
        return Response(serializer.data)
    
class AssessmentDetailView(APIView):
    def get(self, request,pk):
        reservation = Assessment.objects.get(pk=pk)
        serializer=AssessmentSerializer(reservation)
        return Response(serializer.data)

class AssessmentCreateView(APIView):
    def post(self, request):
        serializer = AssessmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssessmentUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Assessment.objects.get(pk=pk)
        except Assessment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        assessment = self.get_object(pk)
        serializer = AssessmentSerializer(assessment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssessmentDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Assessment.objects.get(pk=pk)
        except Assessment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        assessment = self.get_object(pk)
        assessment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    
