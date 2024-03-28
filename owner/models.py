from django.db import models
from django.core.exceptions import ValidationError
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
    name = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField()
    phoneNumber=models.IntegerField()
    address=models.CharField(max_length=250)
    customer_id = models.CharField(max_length=50, unique=True, null = True, default=None, blank=True)

    userCustom = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def validate_phone_number_length(value):
        if len(str(value)) != 9:
            raise ValidationError('The phone number must be exactly 9 digits.')
        
    def __str__(self):
        return f"Owner - {self.name} {self.lastName} ({self.id})"