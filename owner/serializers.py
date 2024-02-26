from rest_framework import serializers
from .models import Owner
from .models import CustomUser

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'

    def validate_userCustom(self, value):
        """
        Comprobar si existe el user proporcionado.
        """
        if not CustomUser.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("User does not exist.")
        return value
    
    def validate_phoneNumber(self, value):
        """
        Comprobar si el número de teléfono tiene 9 dígitos.
        """
        if len(str(value)) != 9:
            raise serializers.ValidationError("Phone number must be a 9-digit number.")
        return value