from rest_framework import serializers
from .models import Equipment

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'brand', 'serial_number', 'description', 'muscular_group', 'assessment']

    def validate_assessment(self, value):
        
        if value < 0 or value > 10:
            raise serializers.ValidationError("Assessment must be between 0 and 10.")
        return value