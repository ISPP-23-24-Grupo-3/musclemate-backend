from django.db import models
from client.models import Client
from gym.models import Gym
from django.core.validators import RegexValidator
from equipment.models import Equipment
from random import randint

class Ticket(models.Model):

    def random_id():
        return randint(100000, 999999)
    
    
    id = models.PositiveIntegerField(primary_key=True, default=random_id, editable=False)
    label = models.CharField(max_length=50)
    description = models.CharField(max_length=250, validators=[RegexValidator(r'^[a-z, A-Z]', message="La descripción debe contener letras.")])
    status = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True )


    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)


    def __str__(self):
        return f"Ticket - {self.equipment.name}, {self.client.name} {self.client.lastName}, {self.date} ({self.id})"