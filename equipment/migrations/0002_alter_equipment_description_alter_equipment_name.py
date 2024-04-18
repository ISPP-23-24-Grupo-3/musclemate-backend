# Generated by Django 4.2.7 on 2024-04-08 11:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='description',
            field=models.TextField(validators=[django.core.validators.RegexValidator('^[a-z, A-Z]', message='La descripción debe contener letras.')]),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('^[a-z, A-Z]', message='El nombre debe contener letras.')]),
        ),
    ]
