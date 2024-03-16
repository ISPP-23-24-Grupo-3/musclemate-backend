from rest_framework import serializers
from .models import Routine,Workout,Client,Equipment


class WorkoutSerializer(serializers.ModelSerializer):
    
    client_id = serializers.IntegerField(source='client.id', read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    routine = serializers.PrimaryKeyRelatedField(queryset=Routine.objects.all(), many=True)
    equipment = serializers.PrimaryKeyRelatedField(queryset=Equipment.objects.all(), many=True)
    class Meta:
        model = Workout
        fields = ['id','name','client_id', 'client_name', 'routine', 'equipment']
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['routine'] = [routine.id for routine in instance.routine.all()] if instance.routine else None
        ret['equipment'] = [equipment.id for equipment in instance.equipment.all()] if instance.equipment else None
        return ret
      
class WorkoutCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'name', 'routine', 'equipment', 'client']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['routine'] = [routine.id for routine in instance.routine.all()] if instance.routine else None
        ret['equipment'] = [equipment.id for equipment in instance.equipment.all()] if instance.equipment else None
        return ret
    
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
        for routine in value:
            if not Routine.objects.filter(id=routine.id).exists():
                raise serializers.ValidationError("Routine does not exist.")
        return value
    
    def validate_equipment(self, value):
        """
        Comprobar si existe el equipo proporcionado.
        """
        for equipment in value:
            if not Equipment.objects.filter(id=equipment.id).exists():
                raise serializers.ValidationError("Equipment does not exist.")
        return value