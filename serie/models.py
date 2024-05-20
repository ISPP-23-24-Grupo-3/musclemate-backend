from django.db import models
from workout.models import Workout
from random import randint
from django.core.validators import MinValueValidator


class Serie(models.Model):
    def random_id():
        return randint(100000, 999999)
    
    id = models.PositiveIntegerField(primary_key=True, default=random_id, editable=False)
    reps = models.PositiveIntegerField(validators=[MinValueValidator(1, message=("Las repeticiones deben ser mayores a 0."))])
    weight = models.PositiveIntegerField(validators=[MinValueValidator(1, message=("El peso debe ser mayor a 0."))])
    date = models.DateField()
    duration = models.FloatField()


    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)

    def __str__(self):
        return f"Serie - {self.workout.name}, {self.date} ({self.id})"
