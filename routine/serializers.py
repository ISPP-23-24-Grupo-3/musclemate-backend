from rest_framework import serializers
from .models import Routine

class RoutineSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.username', read_only=True)

    class Meta:
        model = Routine
        fields = '__all__'