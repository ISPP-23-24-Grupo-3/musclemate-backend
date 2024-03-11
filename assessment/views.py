from equipment.models import Equipment
from .models import Assessment,Client
from rest_framework.response import Response
from .serializers import AssessmentSerializer
from rest_framework import status
from rest_framework.views import APIView

class AssessmentListView(APIView):
    def get(self, request):
        if request.user.rol=='gym' or request.user.rol=='owner':
            assessments = Assessment.objects.all()
            serializer=AssessmentSerializer(assessments,many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)
    
class AssessmentListByClientView(APIView):
    def get(self, request,clientId):
        clientIdByUser=Client.objects.get(user=request.user).id
        if clientIdByUser == clientId and Client.objects.get(id=clientIdByUser).register:
            assessments = Assessment.objects.filter(client=clientId)
            serializer=AssessmentSerializer(assessments,many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)
    
class AssessmentDetailView(APIView):
    def get(self, request,pk):
        clientIdByUser=Client.objects.get(user=request.user).id
        clientIdByAssesstment=Assessment.objects.get(pk=pk).client.id
        if clientIdByUser == clientIdByAssesstment and Client.objects.get(id=clientIdByUser).register:
            reservation = Assessment.objects.get(pk=pk)
            serializer=AssessmentSerializer(reservation)
            return Response(serializer.data)
        else:
            return Response(status=403)

class AssessmentCreateView(APIView):
    def post(self, request):
        gymIdByEquipment=Equipment.objects.get(pk=request.data.get('equipment')).gym.id
        gymIdByclient=Client.objects.get(pk=request.data.get('client')).gym.id
        if not Assessment.objects.filter(client=request.data.get('client'),
            equipment=request.data.get('equipment')).exists() and gymIdByEquipment==gymIdByclient:
            serializer = AssessmentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Assesstment already exists',status=status.HTTP_400_BAD_REQUEST)

class AssessmentUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Assessment.objects.get(pk=pk)
        except Assessment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        clientIdByUser=Client.objects.get(user=request.user).id
        clientIdByAssesstment=request.data.get('client')
        if clientIdByUser == clientIdByAssesstment and Client.objects.get(id=clientIdByUser).register:
            assessment = self.get_object(pk)
            serializer = AssessmentSerializer(assessment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        else:
            return Response(status=403)

class AssessmentDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Assessment.objects.get(pk=pk)
        except Assessment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        clientIdByUser=Client.objects.get(user=request.user).id
        clientIdByAssesstment=Assessment.objects.get(pk=pk).client.id
        if clientIdByUser == clientIdByAssesstment and Client.objects.get(id=clientIdByUser).register:
            assessment = self.get_object(pk)
            assessment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=403)
    

    
