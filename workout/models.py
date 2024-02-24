from django.db import models
from routine.models import Routine
from client.models import Client

class Workout(models.Model):
    name = models.CharField(max_length=100,unique=True)

    routine = models.ManyToManyField(Routine)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.name