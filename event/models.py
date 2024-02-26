from django.db import models
from gym.models import Gym

class Event(models.Model):
    INTENSITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    instructor = models.CharField(max_length=100)
    date = models.DateField()
    isClickable = models.BooleanField()
    duration = models.DateTimeField()
    intensity = models.CharField(max_length=1, choices=INTENSITY_CHOICES, blank=True, null=True)
    isNotice = models.BooleanField()

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)