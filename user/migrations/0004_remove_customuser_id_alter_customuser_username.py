# Generated by Django 5.0.2 on 2024-02-28 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_customuser_rol'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='id',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
