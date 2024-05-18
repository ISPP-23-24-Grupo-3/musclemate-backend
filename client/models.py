from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from user.models import CustomUser
from gym.models import Gym
from random import randint
from django.core.exceptions import ValidationError
from django.utils import timezone

class Client (models.Model):
    
    def random_id():
        return randint(100000, 999999)
    
    id = models.PositiveIntegerField(primary_key=True, default=random_id, editable=False)
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    name = models.CharField(max_length=100, validators=[RegexValidator(r'^[a-zA-Z\s]*$', message="El nombre debe contener solo letras.")])
    last_name = models.CharField(max_length=100, validators=[RegexValidator(r'^[a-zA-Z\s]*$', message="El nombre debe contener solo letras.")])
    email = models.EmailField()
    birth = models.DateField(blank=True, null=True)
    zipCode = models.CharField(max_length=5, validators=[RegexValidator(r'^[0-9]{5}$', message="El código postal debe contener 5 dígitos numéricos.")])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    phone_number = models.CharField(max_length=9, validators=[RegexValidator(r'^[0-9]{9}$',
        message="El número de teléfono debe contener solo dígitos y una longitud de 9 dígitos.")])
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    register = models.BooleanField()

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

    def __str__(self):
        return f"Client - {self.name} {self.last_name} ({self.id})"
    
    def validate_unique_email(self):
        existing_clients = Client.objects.exclude(pk=self.pk).filter(email=self.email)
        if existing_clients.exists():
            raise ValidationError({"email": ("Este correo electrónico ya está en uso")})

    
    def validate_adult_age(self):
        if self.birth:
            adult_age = 18
            delta = timezone.now().date() - self.birth
            if delta.days < adult_age * 365:
                raise ValidationError({'birth': ('El cliente debe ser mayor de edad para registrarse.')})
    
    def clean(self):
        super().clean()
        self.validate_unique_email()
        self.validate_adult_age()