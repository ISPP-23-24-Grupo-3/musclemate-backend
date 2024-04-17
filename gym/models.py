from django.db import models
from owner.models import Owner
from user.models import CustomUser
from django.core.validators import RegexValidator
from random import randint

class Gym(models.Model):
    def random_id():
        return randint(100000, 999999)
    
    SUBSCRIPTION_CHOICE = (
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('free', 'Free')
    )
    
    id = models.PositiveIntegerField(primary_key=True, default=random_id, editable=False)
    name = models.CharField(max_length = 50, validators=[RegexValidator(r'^[a-z, A-Z]', message="El nombre debe contener letras.")])
    address = models.CharField(max_length = 200,validators=[RegexValidator(r'^[a-z, A-Z]', message="La dirección debe contener letras.")])
    phone_number = models.CharField(max_length=9, validators=[RegexValidator(r'^[0-9]{9}',
        message="El número de teléfono debe contener solo dígitos y una longitud de 6 dígitos.")])
    descripcion = models.CharField(max_length = 500)
    zip_code = models.CharField(max_length=5, validators=[RegexValidator(r'^[0-9]{5}$', message="El código postal debe contener 5 dígitos numéricos.")])
    email = models.EmailField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    userCustom = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    subscription_plan = models.CharField(max_length=50, choices=SUBSCRIPTION_CHOICE, default='free', null = True)

    def __str__(self):
        return f"Gym - {self.name} ({self.id})"
