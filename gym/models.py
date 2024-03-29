from django.db import models
from owner.models import Owner
from user.models import CustomUser
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
    name = models.CharField(max_length = 50)
    address = models.CharField(max_length = 200)
    phone_number = models.IntegerField()
    descripcion = models.CharField(max_length = 500)
    zip_code = models.IntegerField()
    email = models.EmailField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    userCustom = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    subscription_plan = models.CharField(max_length=50, choices=SUBSCRIPTION_CHOICE, default=None, null = True)

    def __str__(self):
        return f"Gym - {self.name} ({self.id})"
