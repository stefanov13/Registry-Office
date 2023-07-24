# Generated by Django 4.2.3 on 2023-07-24 13:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OutgoingLogModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_num', models.IntegerField(editable=False, unique=True, verbose_name="Log's number")),
                ('title', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Полето трябва да съдържа поне 2 букви')], verbose_name='Title')),
                ('recipient', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Полето трябва да съдържа поне 2 букви')], verbose_name='Recipient')),
                ('signatory_name', models.CharField(max_length=70)),
                ('signatory_position', models.CharField(max_length=70)),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('document_img', models.ImageField(blank=True, null=True, upload_to='outgoing_doc_img')),
            ],
        ),
    ]
