# Generated by Django 5.0.2 on 2024-02-28 12:40

import equipment.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='id',
            field=models.PositiveIntegerField(default=equipment.models.Equipment.random_id, editable=False, primary_key=True, serialize=False),
        ),
    ]
