from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from user.models import CustomUser
from random import randint

class Owner(models.Model):
    def random_id():
        return randint(100000, 999999)
    
    id = models.PositiveIntegerField(primary_key=True, default=random_id, editable=False)
    INTENSITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]
    name = models.CharField(max_length=100, validators=[RegexValidator(r'^[a-zA-Z\s]*$', message="El nombre debe contener solo letras.")])
    last_name = models.CharField(max_length=100, validators=[RegexValidator(r'^[a-zA-Z\s]*$', message="El nombre debe contener solo letras.")])
    email = models.EmailField()
    phone_number = models.CharField(max_length=9, validators=[RegexValidator(r'^[0-9]{9}$',
        message="El número de teléfono debe contener solo dígitos y una longitud de 9 dígitos.")])
    address=models.CharField(max_length=250)
    customer_id = models.CharField(max_length=50, unique=True, null = True, default=None, blank=True)

    userCustom = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  
    def __str__(self):
        return f"Owner - {self.name} {self.last_name} ({self.id})"
    
    def clean(self):
        super().clean()
        if CustomUser.objects.filter(email=self.email).exists():
            raise ValidationError({"email": ("Este correo electrónico ya está en uso")})