from rest_framework import serializers
from .models import CustomUser

from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    gym_name = serializers.CharField(source='gym.name', read_only=True)
    client_name = serializers.CharField(source='client.username', read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'label', 'description', 'gym_name', 'client_name']
