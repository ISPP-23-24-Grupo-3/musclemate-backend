from django.db import models
from workout.models import Workout

class Serie(models.Model):
    reps = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    date = models.DateField()


    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
