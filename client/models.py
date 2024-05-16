from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from user.models import CustomUser
from gym.models import Gym
from random import randint
class Client (models.Model):
    
    def random_id():
        return randint(100000, 999999)
    
    id = models.PositiveIntegerField(primary_key=True, default=random_id, editable=False)
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    name = models.CharField(max_length=100, validators=[MinLengthValidator(1), MaxLengthValidator(100)])
    last_name = models.CharField(max_length=100, validators=[MinLengthValidator(1), MaxLengthValidator(100)])
    email = models.EmailField(unique = True)
    birth = models.DateField(blank=True, null=True)
    zipCode = models.PositiveIntegerField(validators=[RegexValidator(r'^[0-9]{5}$', message="El código postal debe contener 5 dígitos numéricos.")])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    phone_number = models.PositiveIntegerField(validators=[RegexValidator(r'^[0-9]{9}', message="El número de teléfono debe contener solo dígitos y una longitud de 9 dígitos.")])
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    register = models.BooleanField()

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

    def __str__(self):
        return f"Client - {self.name} {self.last_name} ({self.id})"

