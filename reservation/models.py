from django.db import models
from client.models import Client
from event.models import Event
from random import randint
class Reservation (models.Model):
    def random_id():
        return randint(100000, 999999)
    
    id = models.PositiveIntegerField(primary_key=True, default=random_id, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)