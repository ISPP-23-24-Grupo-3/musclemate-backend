from django.db import models
from django.core.exceptions import ValidationError
from user.models import CustomUser
from gym.models import Gym

class Client (models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    birth = models.DateField(blank=True, null=True)
    zip_code = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    phone_number = models.PositiveIntegerField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    register = models.BooleanField()

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)


    def validate_phone_number_length(value):
        if len(str(value)) != 9:
            raise ValidationError('The phone number must be exactly 9 digits.')

    def __str__(self):
        return f"{self.name} {self.last_name}"

