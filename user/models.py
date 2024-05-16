from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from .managermodel import CustomUserManager
from random import randint
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError

from .validators import UnicodeUsernameValidator


class CustomUser(AbstractBaseUser, PermissionsMixin):
    def random_id():
        return randint(100000, 999999)

    def gen_verification_token(self):
        return default_token_generator.make_token(self)

    ROL_CHOICES = (
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('owner', 'Owner'),
        ('gym', 'Gym')
    )

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=_(
            "Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente."
        ),
        primary_key=True,
        validators=[username_validator],
        error_messages={
            "unique": _("Ya existe un usuario con este nombre de usuario."),
        },
    )
    id = models.IntegerField(primary_key=False, auto_created=True,default=random_id, editable=False)
    first_name = models.CharField(max_length=30, blank=True, validators=[MinLengthValidator(1), MaxLengthValidator(30)])
    last_name = models.CharField(max_length=150, blank=True, validators=[MinLengthValidator(1), MaxLengthValidator(150)])
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    rol = models.CharField(max_length=100, choices=ROL_CHOICES, default='client')
    is_verified = models.BooleanField(default=False)
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

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    
    def clean(self):
        super().clean()
        if CustomUser.objects.filter(email=self.email).exists():
            raise ValidationError({"email": _("Este correo electrónico ya está en uso")})