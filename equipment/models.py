from django.db import models
from gym.models import Gym
from django.core.validators import RegexValidator
from random import randint
from django.contrib.postgres.fields import ArrayField


class Equipment(models.Model):
    def random_id():
        return randint(100000, 999999)

    id = models.PositiveIntegerField(
        primary_key=True, default=random_id, editable=False
    )

    MUSCULAR_GROUP_CHOICES = (
        ("arms", "Arms"),
        ("legs", "Legs"),
        ("core", "Core"),
        ("chest", "Chest"),
        ("back", "Back"),
        ("shoulders", "Shoulders"),
        ("other", "Other"),
    )

    name = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(r"^[a-z, A-Z]", message="El nombre debe contener letras.")
        ],
    )
    brand = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    image = models.ImageField(upload_to="equipment_images/", blank=True, null=True)
    description = models.TextField(
        validators=[
            RegexValidator(
                r"^[a-z, A-Z]", message="La descripción debe contener letras."
            )
        ]
    )
    muscular_groups = models.CharField(
        max_length=100,
        help_text="Selecciona los grupos musculares separados por comas, ej: 'arms,legs,core'"
    )
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("serial_number", "gym")

    def __str__(self):
        return f"Equipment - {self.name}, {self.brand} ({self.id})"
