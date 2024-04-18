# Generated by Django 4.2.7 on 2024-04-18 19:07

from django.db import migrations, models
import django.db.models.deletion
import routine.models


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
