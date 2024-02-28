from django.db import models
from random import randint
from django.core.validators import MinValueValidator, MaxValueValidator
from equipment.models import Equipment


class Assessment(models.Model):
    def random_id():
        return randint(100000, 999999)
    
    id = models.PositiveIntegerField(primary_key=True, default=random_id, editable=False)

    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
