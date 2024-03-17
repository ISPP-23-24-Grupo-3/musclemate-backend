# Generated by Django 5.0.2 on 2024-03-17 09:12

import django.db.models.deletion
import routine.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Routine',
            fields=[
                ('id', models.PositiveIntegerField(default=routine.models.Routine.random_id, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=60)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
            ],
            options={
                'unique_together': {('name', 'client')},
            },
        ),
    ]
