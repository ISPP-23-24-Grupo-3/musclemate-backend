# Generated by Django 4.2.7 on 2024-04-08 11:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_alter_client_phonenumber_alter_client_zipcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phoneNumber',
            field=models.PositiveIntegerField(validators=[django.core.validators.RegexValidator('^[0-9]{9}', message='El número de teléfono debe contener solo dígitos y una longitud de 6 dígitos.')]),
        ),
        migrations.AlterField(
            model_name='client',
            name='zipCode',
            field=models.PositiveIntegerField(validators=[django.core.validators.RegexValidator('^[0-9]{5}$', message='El código postal debe contener 5 dígitos numéricos.')]),
        ),
    ]
