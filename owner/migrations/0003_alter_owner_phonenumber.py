# Generated by Django 4.2.7 on 2024-04-17 15:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0002_alter_owner_lastname_alter_owner_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='phoneNumber',
            field=models.PositiveIntegerField(
                validators=[django.core.validators.RegexValidator('^[0-9]{6}',
                message='El número de teléfono debe contener solo dígitos y una longitud de 6 dígitos.')]
            ),
        ),
    ]
