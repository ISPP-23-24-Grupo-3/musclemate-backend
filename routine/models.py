from django.db import models
from client.models import Client


# Create your models here.

class Routine(models.Model):
    
    name = models.CharField(max_length=60)

    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'client')

    def __str__(self):
        return self.name