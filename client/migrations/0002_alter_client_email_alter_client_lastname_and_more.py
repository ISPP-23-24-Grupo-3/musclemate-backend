# Generated by Django 4.2.7 on 2024-04-07 17:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='lastName',
            field=models.CharField(
                max_length=100,
                validators=[django.core.validators.MinLengthValidator(1), 
                django.core.validators.MaxLengthValidator(100)]
            ),
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(
                max_length=100,
                validators=[django.core.validators.MinLengthValidator(1),
                django.core.validators.MaxLengthValidator(100)]
            ),
        ),
        migrations.AlterField(
            model_name='client',
            name='phoneNumber',
            field=models.PositiveIntegerField(
                max_length=6,
                validators=[django.core.validators.MinLengthValidator(6),
                django.core.validators.MaxLengthValidator(6),
                django.core.validators.RegexValidator('^[0-9]+$',
                message='El número de teléfono debe contener solo dígitos.')]
            ),
        ),
        migrations.AlterField(
            model_name='client',
            name='zipCode',
            field=models.PositiveIntegerField(
                max_length=5,
                validators=[django.core.validators.MinLengthValidator(5),
                django.core.validators.MaxLengthValidator(5), 
                django.core.validators.RegexValidator('^[0-9]{5}$',
                message='El código postal debe contener 5 dígitos numéricos.')]
            ),
        ),
    ]
