from django.db import models
from django.core.exceptions import ValidationError
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
    name = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField()
    birth = models.DateField(blank=True, null=True)
    zipCode = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    phoneNumber = models.PositiveIntegerField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    register = models.BooleanField()

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)


