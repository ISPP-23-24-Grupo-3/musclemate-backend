from rest_framework import serializers
from .models import Ticket
from client.serializers import ClientSerializer

class TicketViewSerializer(serializers.ModelSerializer):
    gym_name = serializers.CharField(source='gym.name', read_only=True)
    client = ClientSerializer()
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'label', 'description', 'status', 'date','gym','gym_name','client','equipment','equipment_name']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['label', 'description', 'equipment']

class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['label', 'description', 'equipment', 'status']

