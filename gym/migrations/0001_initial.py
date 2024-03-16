# Generated by Django 4.2.7 on 2024-03-16 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import gym.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('owner', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gym',
            fields=[
                ('id', models.PositiveIntegerField(default=gym.models.Gym.random_id, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('phone_number', models.IntegerField()),
                ('descripcion', models.CharField(max_length=500)),
                ('zip_code', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='owner.owner')),
                ('userCustom', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
