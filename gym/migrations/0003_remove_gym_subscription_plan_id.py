# Generated by Django 4.2.7 on 2024-03-29 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0002_gym_subscription_plan_gym_subscription_plan_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gym',
            name='subscription_plan_id',
        ),
    ]
