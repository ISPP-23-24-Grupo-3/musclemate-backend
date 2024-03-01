from django.db import models
from routine.models import Routine
from client.models import Client
from equipment.models import Equipment

class Workout(models.Model):
    name = models.CharField(max_length=100,unique=True)

    routine = models.ManyToManyField(Routine)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    equipment = models.ManyToManyField(Equipment, blank=True)