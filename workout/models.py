from django.db import models
from routine.models import Routine
from client.models import Client
from equipment.models import Equipment
from random import randint
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator

class Workout(models.Model):
    def random_id():
        return randint(100000, 999999)
    
    
    id = models.PositiveIntegerField(primary_key=True, default=random_id, editable=False)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(1), MaxLengthValidator(100)])

    routine = models.ManyToManyField(Routine, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    equipment = models.ManyToManyField(Equipment, blank=True)
        
    def __str__(self):
        return f"Workout - {self.name}, {self.client.name} {self.client.lastName} ({self.id})"
