# Generated by Django 4.2.3 on 2023-08-10 07:40

import core.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2, 'Името трябва да съдържа поне 2 букви'), core.validators.name_cyrillic_letters_and_hyphens_validator], verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2, 'Фамилията трябва да съдържа поне 2 букви'), core.validators.name_cyrillic_letters_and_hyphens_validator], verbose_name='Last Name')),
                ('position', models.CharField(max_length=70, validators=[django.core.validators.MinLengthValidator(2, 'Длъжността трябва да съдържа поне 2 букви'), core.validators.position_field_validator], verbose_name='Position')),
                ('owner', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
