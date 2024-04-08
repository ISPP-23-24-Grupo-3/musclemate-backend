from rest_framework import serializers
from .models import Client
from .models import Reservation
from .models import Event

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


    def validate_client(self, value):
        """
        Comprobar si existe el cliente proporcionado.
        """
        if not Client.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Client does not exist.")
        return value
    
    def validate_event(self, value):
        """
        Comprobar si existe el evento proporcionado.
        """
        if not Event.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Event does not exist.")
        return value
    
class ReservationUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['event']
    
    def validate_event(self, value):
        """
        Comprobar si existe el evento proporcionado.
        """
        if not Event.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Event does not exist.")
        return value