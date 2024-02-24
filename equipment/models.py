from django.db import models
from django.contrib.auth.models import AbstractUser

class Equipment(AbstractUser):
    MUSCULAR_GROUP_CHOICES = (
        ('arms', 'Arms'),
        ('legs', 'Legs'),
        ('core', 'Core'),
        ('chest', 'Chest'),
        ('back', 'Back'),
        ('shoulders', 'Shoulders'),
        ('other', 'Other')
    )

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    description = models.TextField()
    muscular_group = models.CharField(max_length=20, choices=MUSCULAR_GROUP_CHOICES)
    assessment = models.FloatField()
    gym = models.ForeignKey(gym, on_delete=models.Cascade)

    class Meta:
        unique_together = ('serial_number', 'gym')

    def __str__(self):
        return self.name