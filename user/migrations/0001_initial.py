# Generated by Django 5.0.2 on 2024-05-20 19:50

import django.core.validators
import django.utils.timezone
import user.models
import user.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.IntegerField(auto_created=True, default=user.models.CustomUser.random_id, editable=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'Ya existe un usuario con este nombre de usuario.'}, help_text='Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.', max_length=150, primary_key=True, serialize=False, unique=True, validators=[user.validators.UnicodeUsernameValidator()])),
                ('first_name', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[a-zA-Z\\sáéíóúÁÉÍÓÚ]*$', message='El nombre debe contener solo letras.')])),
                ('last_name', models.CharField(max_length=150, validators=[django.core.validators.RegexValidator('^[a-zA-Z\\sáéíóúÁÉÍÓÚ]*$', message='El nombre debe contener solo letras.')])),
                ('email', models.EmailField(error_messages={'unique': 'Ya existe un usuario con este correo electrónico.'}, max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('rol', models.CharField(choices=[('admin', 'Admin'), ('client', 'Client'), ('owner', 'Owner'), ('gym', 'Gym')], default='client', max_length=100)),
                ('is_verified', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='custom_user_groups', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='custom_user_permissions', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
