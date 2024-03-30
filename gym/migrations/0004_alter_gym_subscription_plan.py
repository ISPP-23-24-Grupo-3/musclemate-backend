# Generated by Django 4.2.7 on 2024-03-29 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0003_remove_gym_subscription_plan_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gym',
            name='subscription_plan',
            field=models.CharField(choices=[('standard', 'Standard'), ('premium', 'Premium'), ('free', 'Free')], default=None, max_length=50, null=True),
        ),
    ]
