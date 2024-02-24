from rest_framework import serializers
from .models import Equipment

class EquipmentSerializer(serializers.ModelSerializer):
    gym_name = serializers.CharField(source='gym.username', read_only=True)

    class Meta:
        model = Equipment
        fields = ['name', 'brand', 'serial_number', 'description', 'muscular_group', 'assessment', 'gym_name']

    def validate_assessment(self, value):
        
        if value < 0 or value > 10:
            raise serializers.ValidationError("Assessment must be between 0 and 10.")
        return value