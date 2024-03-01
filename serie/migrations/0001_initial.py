# Generated by Django 4.2.7 on 2024-02-28 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workout', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reps', models.PositiveIntegerField()),
                ('weight', models.PositiveIntegerField()),
                ('date', models.DateField()),
                ('workout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout.workout')),
            ],
        ),
    ]
