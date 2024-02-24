from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Routine(AbstractUser):
    
    name = models.CharField(max_length=60)

    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'client')

    def __str__(self):
        return self.name