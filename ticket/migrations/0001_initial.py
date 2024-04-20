# Generated by Django 5.0.2 on 2024-04-20 19:44

import django.core.validators
import django.db.models.deletion
import ticket.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
        ('equipment', '0001_initial'),
        ('gym', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.PositiveIntegerField(default=ticket.models.Ticket.random_id, editable=False, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250, validators=[django.core.validators.RegexValidator('^[a-z, A-Z]', message='La descripción debe contener letras.')])),
                ('status', models.CharField(blank=True, choices=[('open', 'Open'), ('closed', 'Closed'), ('in progress', 'In progress'), ('seen', 'Seen')],
                                            default='open', max_length=50, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('image', models.URLField(blank=True, null=True)),
                ('response', models.CharField(blank=True, max_length=250, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.equipment')),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gym.gym')),
            ],
        ),
    ]
