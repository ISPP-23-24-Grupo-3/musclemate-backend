from rest_framework import serializers
from .models import Client
from .models import Gym
from .models import CustomUser

class ClientSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    gym = serializers.PrimaryKeyRelatedField(queryset=Gym.objects.all())
    class Meta:
        model = Client
        fields = ['name', 'lastName', 'birth', 'zipCode','gender', 'phoneNumber', 'email','address','city','register', 'user', 'gym']

    def validate_phoneNumber(self, value):
        """
        Comprobar si el número de teléfono tiene 9 dígitos.
        """
        if len(str(value)) != 9:
            raise serializers.ValidationError("Phone number must be a 9-digit number.")
        return value

    def validate_zipCode(self, value):
        """
        Comprobar si el código postal tiene 5 dígitos.
        """
        if len(str(value)) != 5:
            raise serializers.ValidationError("Zip code must be a 5-digit number.")
        return value

    def validate_gym(self, value):
        """
        Comprobar si existe el gimnasio proporcionado.
        """
        if not Gym.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Gym does not exist.")
        return value
    
    def validate_user(self, value):
        """
        Comprobar si existe el user proporcionado.
        """
        if not CustomUser.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("User does not exist.")
        return value