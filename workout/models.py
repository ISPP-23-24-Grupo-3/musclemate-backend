from django.db import models
from routine.models import Routine
from client.models import Client
from equipment.models import Equipment
from random import randint
class Workout(models.Model):
    def random_id():
        return randint(100000, 999999)
    
    
    id = models.PositiveIntegerField(primary_key=True, default=random_id, editable=False)
    name = models.CharField(max_length=100,unique=True)

    routine = models.ManyToManyField(Routine, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    equipment = models.ManyToManyField(Equipment, blank=True)
