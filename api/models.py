from django.db import models

class Gym(models.Model):
    name = models.CharField(max_length = 50)
    address = models.CharField(max_length = 200)
    phone_number = models.IntegerField()
    descripcion = models.CharField(max_length = 500)
    zip_code = models.IntegerField()
    email = models.EmailField()
    #owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
