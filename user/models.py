from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    ROL_CHOICES = (
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('owner', 'Owner'),
        ('gym', 'Gym')
    )

    username = models.CharField(max_length=100, unique=True, primary_key=True)
    rol = models.CharField(max_length=100, choices=ROL_CHOICES, default='client')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username