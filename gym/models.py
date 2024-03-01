from django.db import models
from owner.models import Owner
from user.models import CustomUser

class Gym(models.Model):
    name = models.CharField(max_length = 50)
    address = models.CharField(max_length = 200)
    phone_number = models.IntegerField()
    descripcion = models.CharField(max_length = 500)
    zip_code = models.IntegerField()
    email = models.EmailField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    userCustom = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
