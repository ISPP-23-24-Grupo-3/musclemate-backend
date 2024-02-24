from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Ticket(AbstractUser):

    label = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


    def __str__(self):
        return self.label