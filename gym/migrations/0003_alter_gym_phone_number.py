# Generated by Django 4.2.7 on 2024-05-18 11:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0002_alter_gym_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gym',
            name='phone_number',
            field=models.CharField(max_length=9, validators=[django.core.validators.RegexValidator('^[0-9]{9}$', message='El número de teléfono debe contener solo dígitos y una longitud de 9 dígitos.')]),
        ),
    ]
