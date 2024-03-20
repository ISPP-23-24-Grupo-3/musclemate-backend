from django.db import models
from random import randint
from django.core.validators import MinValueValidator, MaxValueValidator
from equipment.models import Equipment
from client.models import Client


class Assessment(models.Model):
    def random_id():
        return randint(100000, 999999)
    
    id = models.PositiveIntegerField(primary_key=True, default=random_id, editable=False)

    stars = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"Assesment - {self.equipment.name}, {self.client.name} {self.client.lastName} ({self.id})"
