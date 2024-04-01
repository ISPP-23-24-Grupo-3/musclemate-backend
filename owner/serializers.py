from rest_framework import serializers
from .models import Owner
from .models import CustomUser
from user.serializers import CustomUserSerializer

class OwnerSerializer(serializers.ModelSerializer):
    userCustom = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    class Meta:
        model = Owner
        fields = ['name', 'lastName', 'email', 'phoneNumber', 'address', 'userCustom', 'customer_id']

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