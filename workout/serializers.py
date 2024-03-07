from rest_framework import serializers
from .models import Routine,Workout,Client,Equipment


class WorkoutSerializer(serializers.ModelSerializer):
    
    client_id = serializers.IntegerField(source='client.id', read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    routine_name = serializers.CharField(source='routine.name', read_only=True)
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    equipment_brand = serializers.CharField(source='equipment.brand', read_only=True)
    equipment_serial_number = serializers.CharField(source='equipment.serial_number', read_only=True)
    equipment_muscular_group = serializers.CharField(source='equipment.muscular_group', read_only=True)
    equipment_description = serializers.CharField(source='equipment.description', read_only=True)
    equipment_id = serializers.IntegerField(source='equipment.id', read_only=True)
    class Meta:
        model = Workout
        fields = ['id','name','client','client_id', 'client_name', 'routine_name', 'equipment_name', 'equipment_brand', 'equipment_serial_number', 'equipment_muscular_group', 'equipment_description', 'equipment_id']

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