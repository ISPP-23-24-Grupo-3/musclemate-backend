from django.db import models
from gym.models import Gym
from random import randint
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator


class Event(models.Model):

    def random_id():
        return randint(100000, 999999)
    
    id = models.PositiveIntegerField(primary_key=True, default=random_id, editable=False)
    INTENSITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]
    name = models.CharField(max_length=100, validators=[RegexValidator(r'^[a-z, A-Z]', message="El nombre debe contener letras.")])
    description = models.CharField(max_length=255, validators=[RegexValidator(r'^[a-z, A-Z]', message="La descripción debe contener letras.")])
    capacity = models.PositiveIntegerField()
    attendees = models.PositiveIntegerField()
    instructor = models.CharField(max_length=100)
    date = models.DateField()
    isClickable = models.BooleanField(default=False, blank=True, null=True)
    duration = models.DurationField()
    intensity = models.CharField(max_length=1, choices=INTENSITY_CHOICES, blank=True, null=True)
    isNotice = models.BooleanField(default=False, blank=True, null=True)

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

    def __str__(self):
        return f"Event - {self.name}, {self.gym.name} ({self.id})"