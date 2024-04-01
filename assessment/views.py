from equipment.models import Equipment
from user.models import CustomUser
from .models import Assessment,Client
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import AssessmentSerializer
from rest_framework import status
from rest_framework.views import APIView

@permission_classes([IsAuthenticated])
class AssessmentListView(APIView):
    def get(self, request):
            assessments = Assessment.objects.all()
            serializer=AssessmentSerializer(assessments,many=True)
            return Response(serializer.data)

@permission_classes([IsAuthenticated])
class AssessmentListByClientView(APIView):
    def get(self, request,clientId):
        assessments = Assessment.objects.filter(client=clientId)
        serializer=AssessmentSerializer(assessments,many=True)
        return Response(serializer.data)

@permission_classes([IsAuthenticated])
class AssessmentListByEquipmentView(APIView):
    def get(self, request,equipmentId):
        if request.user.rol=='client':
            user = CustomUser.objects.get(username=request.user)
            client = Client.objects.get(user=user)
            if client.gym.id == Equipment.objects.get(pk=equipmentId).gym.id:
                assessments = Assessment.objects.filter(client=client.id, equipment=equipmentId)
                serializer=AssessmentSerializer(assessments,many=True)
            else:
                return Response(status=403)
        elif request.user.rol=='owner' or request.user.rol=='gym':
            if (Equipment.objects.get(pk=equipmentId).gym.userCustom == request.user
            or Equipment.objects.get(pk=equipmentId).gym.owner.userCustom == request.user):
                assessments = Assessment.objects.filter(equipment=equipmentId)
                serializer=AssessmentSerializer(assessments,many=True)
            else:
                return Response(status=403)
        return Response(serializer.data)

@permission_classes([IsAuthenticated])
class AssessmentDetailView(APIView):
    def get(self, request,pk):
        assesment = Assessment.objects.get(pk=pk)
        serializer=AssessmentSerializer(assesment)
        return Response(serializer.data)

@permission_classes([IsAuthenticated])
class AssessmentCreateView(APIView):
    def post(self, request):
        if request.user.rol=='client':
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
        else:
            return Response(status=403)

@permission_classes([IsAuthenticated])
class AssessmentUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Assessment.objects.get(pk=pk)
        except Assessment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        if request.user.rol=='client':
            clientIdByUser=Client.objects.get(user=request.user).id
            clientIdByAssesstment=request.data.get('client')
            if clientIdByUser == int(clientIdByAssesstment) and Client.objects.get(id=clientIdByUser).register:
                assessment = self.get_object(pk)
                serializer = AssessmentSerializer(assessment, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            else:
                return Response(status=403)
        else:
            return Response(status=403)

@permission_classes([IsAuthenticated])
class AssessmentDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Assessment.objects.get(pk=pk)
        except Assessment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if request.user.rol=='client':
            clientIdByUser=Client.objects.get(user=request.user).id
            clientIdByAssesstment=Assessment.objects.get(pk=pk).client.id
            if clientIdByUser == clientIdByAssesstment and Client.objects.get(id=clientIdByUser).register:
                assessment = self.get_object(pk)
                assessment.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=403)
        else:
            return Response(status=403)
    

    
