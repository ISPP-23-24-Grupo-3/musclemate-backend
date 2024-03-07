from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    gym_name = serializers.CharField(source='gym.name', read_only=True)
    client_name = serializers.CharField(source='client.username', read_only=True)
    client_lastname = serializers.CharField(source='client.last_name', read_only=True)
    client_email = serializers.CharField(source='client.email', read_only=True)
    client_birth = serializers.DateField(source='client.birth', read_only=True)
    client_zipcode = serializers.IntegerField(source='client.zipCode', read_only=True)
    client_gender = serializers.CharField(source='client.gender', read_only=True)
    client_phonenumber = serializers.IntegerField(source='client.phoneNumber', read_only=True)
    client_city = serializers.CharField(source='client.city', read_only=True)
    client_register = serializers.BooleanField(source='client.register', read_only=True)
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)

    class Meta:
        model = Ticket
        fields = ['label', 'description', 'gym_name', 'client_name','client_lastname','client_email', 'client_birth', 'client_zipcode', 'client_gender', 'client_phonenumber','client_city','client_register', 'equipment_name']

