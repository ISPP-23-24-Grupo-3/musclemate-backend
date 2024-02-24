from django.db import models
from client.models import Client
from gym.models import Gym
from equipment.models import Equipment


class Ticket(models.Model):

    label = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)


    def __str__(self):
        return self.label