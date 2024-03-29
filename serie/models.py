from django.db import models
from workout.models import Workout
from random import randint

class Serie(models.Model):
    def random_id():
        return randint(100000, 999999)
    
    id = models.PositiveIntegerField(primary_key=True, default=random_id, editable=False)
    reps = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    date = models.DateField()


    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
