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
    name = models.CharField(max_length=100, validators=[MinLengthValidator(1), MaxLengthValidator(100)])
    last_name = models.CharField(max_length=100, validators=[MinLengthValidator(1), MaxLengthValidator(100)])
    email = models.EmailField()
    phone_number=models.PositiveIntegerField(
        validators=[RegexValidator(r'^[0-9]{6}',
        message="El número de teléfono debe contener solo dígitos y una longitud de 6 dígitos.")]
    )
    address=models.CharField(max_length=250)
    customer_id = models.CharField(max_length=50, unique=True, null = True, default=None, blank=True)

    userCustom = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  
    def __str__(self):
        return f"Owner - {self.name} {self.last_name} ({self.id})"