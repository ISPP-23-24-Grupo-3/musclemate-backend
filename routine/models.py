from django.db import models
from client.models import Client
from random import randint

# Create your models here.

class Routine(models.Model):

    def random_id():
        return randint(100000, 999999)
    
    id = models.PositiveIntegerField(primary_key=True, default=random_id, editable=False, unique=True)
    
    name = models.CharField(max_length=60)

    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'client')

    def __str__(self):
        return self.name