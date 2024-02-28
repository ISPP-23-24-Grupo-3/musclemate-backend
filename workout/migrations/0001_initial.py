# Generated by Django 5.0.2 on 2024-02-28 20:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '__first__'),
        ('equipment', '__first__'),
        ('routine', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
                ('equipment', models.ManyToManyField(to='equipment.equipment')),
                ('routine', models.ManyToManyField(to='routine.routine')),
            ],
        ),
    ]
