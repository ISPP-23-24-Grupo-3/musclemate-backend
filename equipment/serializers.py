from rest_framework import serializers
from .models import Equipment
from gym.models import Gym

class EquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipment
        fields = '__all__'

    def validate_gym(self, value):
        """
        Comprobar si existe el gimnasio proporcionado.
        """
        if not Gym.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Gym does not exist.")
        return value