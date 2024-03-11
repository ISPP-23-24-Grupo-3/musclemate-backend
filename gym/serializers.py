from rest_framework import serializers
from .models import Gym, Owner
from owner.models import Owner
from user.models import CustomUser


class GymSerializer(serializers.ModelSerializer):
    userCustom = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    owner = serializers.PrimaryKeyRelatedField(queryset=Owner.objects.all())
    class Meta:
        model = Gym
        fields = ['id','name', 'address', 'zip_code', 'descripcion', 'phone_number', 'email','owner','userCustom']

    def validate_phone_number(self, value):
        """
        Comprobar si el número de teléfono tiene 9 dígitos.
        """
        if len(str(value)) != 9:
            raise serializers.ValidationError("Phone number must be a 9-digit number.")
        return value

    def validate_zip_code(self, value):
        """
        Comprobar si el código postal tiene 5 dígitos.
        """
        if len(str(value)) != 5:
            raise serializers.ValidationError("Zip code must be a 5-digit number.")
        return value

    def validate_owner(self, value):
        """
        Comprobar si existe el dueño proporcionado.
        """
        if not Owner.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Owner does not exist.")
        return value
    
    def validate_userCustom(self, value):
        """

        Comprobar si existe el user proporcionado.

        """
        if not CustomUser.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("User does not exist.")
        return value