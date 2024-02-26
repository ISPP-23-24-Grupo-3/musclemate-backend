from rest_framework import serializers
from .models import Routine,Workout,Client


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = '__all__'

    def validate_client(self, value):
        """
        Comprobar si existe el cliente proporcionado.
        """
        if not Client.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Client does not exist.")
        return value
    
    def validate_routine(self, value):
        """
        Comprobar si existe la rutina proporcionada.
        """
        if not Routine.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Routine does not exist.")
        return value