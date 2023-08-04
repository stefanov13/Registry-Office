# Generated by Django 4.2.3 on 2023-08-04 10:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncomingLogModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_num', models.CharField(editable=False, max_length=15, unique=True, verbose_name="Log's number")),
                ('category', models.CharField(max_length=1)),
                ('title', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Полето трябва да съдържа поне 2 букви')], verbose_name='Title')),
                ('rectors_resolution', models.TextField(blank=True, null=True)),
                ('opinion', models.TextField(blank=True, null=True)),
                ('responsible_persons', models.ManyToManyField(blank=True, to='user_profiles.profile')),
            ],
        ),
    ]
