from rest_framework import serializers
from .models import Serie
from .models import Workout

class SerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serie
        fields = '__all__'

    def validate_workout(self, value):
        """
        Comprobar si existe el workout proporcionado.
        """
        if not Workout.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Workout does not exist.")
        return value

