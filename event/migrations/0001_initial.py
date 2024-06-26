# Generated by Django 5.0.2 on 2024-05-20 19:50

import django.core.validators
import django.db.models.deletion
import event.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gym', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.PositiveIntegerField(default=event.models.Event.random_id, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('^[a-z, A-Z]', message='El nombre debe contener letras.')])),
                ('description', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[a-z, A-Z]', message='La descripción debe contener letras.')])),
                ('capacity', models.PositiveIntegerField()),
                ('attendees', models.PositiveIntegerField()),
                ('instructor', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('isClickable', models.BooleanField(blank=True, default=False, null=True)),
                ('duration', models.DurationField()),
                ('intensity', models.CharField(blank=True, choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High')], max_length=1, null=True)),
                ('isNotice', models.BooleanField(blank=True, default=False, null=True)),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gym.gym')),
            ],
        ),
    ]
