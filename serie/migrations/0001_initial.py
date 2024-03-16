# Generated by Django 5.0.2 on 2024-03-16 17:18

import django.db.models.deletion
import serie.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workout', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.PositiveIntegerField(default=serie.models.Serie.random_id, editable=False, primary_key=True, serialize=False)),
                ('reps', models.PositiveIntegerField()),
                ('weight', models.PositiveIntegerField()),
                ('date', models.DateField()),
                ('duration', models.FloatField()),
                ('workout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout.workout')),
            ],
        ),
    ]
