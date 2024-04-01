# Generated by Django 5.0.2 on 2024-03-25 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gym',
            name='subscription_plan',
            field=models.CharField(choices=[('standard', 'Standard'), ('premium', 'Premium')], default=None, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='gym',
            name='subscription_plan_id',
            field=models.CharField(default=None, max_length=50, null=True, unique=True),
        ),
    ]
