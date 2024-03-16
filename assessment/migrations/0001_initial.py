# Generated by Django 5.0.2 on 2024-03-16 17:18

import assessment.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '__first__'),
        ('equipment', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.PositiveIntegerField(default=assessment.models.Assessment.random_id, editable=False, primary_key=True, serialize=False)),
                ('stars', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.equipment')),
            ],
        ),
    ]
