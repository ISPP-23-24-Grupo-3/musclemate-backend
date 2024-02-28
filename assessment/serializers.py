from rest_framework import serializers
from .models import Assessment

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = '__all__'
    
    def validate_assessment(self, value):
        """
        Comprobar si existe el equipo proporcionado.
        """
        if not Assessment.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Equipment does not exist.")
        return value

