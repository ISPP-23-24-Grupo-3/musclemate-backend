# Generated by Django 5.0.2 on 2024-03-01 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_customuser_rol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='rol',
            field=models.CharField(choices=[('admin', 'Admin'), ('client', 'Client'), ('owner', 'Owner'), ('gym', 'Gym')], default='client', max_length=100),
        ),
    ]
