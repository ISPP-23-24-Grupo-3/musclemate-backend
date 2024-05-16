# Generated by Django 4.2.7 on 2024-05-16 15:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone_number',
            field=models.PositiveIntegerField(validators=[django.core.validators.RegexValidator('^[0-9]{9}', message='El número de teléfono debe contener solo dígitos y una longitud de 9 dígitos.')]),
        ),
    ]
