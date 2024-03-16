# Generated by Django 5.0.2 on 2024-03-16 17:18

from django.db import migrations, models
import django.db.models.deletion
import event.models


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
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('capacity', models.PositiveIntegerField()),
                ('attendees', models.PositiveIntegerField()),
                ('instructor', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('isClickable', models.BooleanField()),
                ('duration', models.DurationField()),
                ('intensity', models.CharField(blank=True, choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High')], max_length=1, null=True)),
                ('isNotice', models.BooleanField()),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gym.gym')),
            ],
        ),
    ]
