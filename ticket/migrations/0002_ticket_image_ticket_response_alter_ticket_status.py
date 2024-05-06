# Generated by Django 4.2.7 on 2024-05-04 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='response',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(blank=True, choices=[
                ('open', 'Open'), ('closed', 'Closed'), ('in progress', 'In progress'), ('seen', 'Seen')
                ], default='open', max_length=50, null=True),
        ),
    ]
