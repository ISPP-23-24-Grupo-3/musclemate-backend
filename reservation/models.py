from django.db import models
from client.models import Client
from event.models import Event

class Reservation (models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)