# Generated by Django 4.2.3 on 2024-01-12 12:02

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrativeOrdersLogModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_num', models.CharField(max_length=7, verbose_name="Log's number")),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation Date')),
                ('title', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Полето трябва да съдържа поне 2 букви')], verbose_name='Title')),
                ('publisher', models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.MinLengthValidator(2, 'Полето трябва да съдържа поне 2 букви')], verbose_name='Publisher')),
                ('document_file', models.FileField(blank=True, null=True, upload_to='outgoing_doc_files', verbose_name='Document File')),
                ('responsible_employees', models.ManyToManyField(blank=True, to='user_profiles.employeepositionsmodel', verbose_name='Responsible Employees')),
            ],
        ),
    ]