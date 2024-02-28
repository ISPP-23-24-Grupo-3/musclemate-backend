from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    ROL_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
        ('owner', 'Owner'),
    )

    username = models.CharField(max_length=100, unique=True)
    rol = models.CharField(max_length=100, choices=ROL_CHOICES, default='user')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username