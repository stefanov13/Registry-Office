# Generated by Django 4.2.3 on 2023-09-04 13:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


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
                ('log_num', models.CharField(max_length=15, unique=True, verbose_name="Log's number")),
                ('category', models.CharField(blank=True, choices=[('РД', 'Ръководна дейност'), ('УД', 'Учебна дейност'), ('ФД', 'Факултетна дейност'), ('ФДСИ', 'Факултетна дейност - "Сценични изкуства"'), ('ФДЕИ', 'Факултетна дейност - "Екранни изкуства"'), ('НИД', 'Научна и издателска дейност'), ('ХТД', 'Художествено - творческа дейност'), ('ХТД_УДТ', 'Худож. - творч. д-ност - Учебен драматичен театър'), ('ХТД_УКТ', 'Худож. - творч. д-ност - Учебен куклен театър'), ('ХТД_УАВК', 'Худож. - творч. д-ност - Учебен аудио визуален комплекс'), ('МС', 'Международно сътрудничество'), ('ПД', 'Проектна дейност'), ('ФСД', 'Финансово  - счетоводна дейност'), ('АПД', 'Административно - правна дейност'), ('ЧР', 'Човешки ресурси'), ('БТ', 'Безопасност на труда'), ('КС', 'Капитално строителство'), ('БД', 'Библиотечна дейност'), ('СС', 'Студентски съвет')], max_length=55, null=True, verbose_name='Category')),
                ('title', models.CharField(max_length=150, validators=[django.core.validators.MinLengthValidator(2, 'Полето трябва да съдържа поне 2 букви')], verbose_name='Title')),
                ('rectors_resolution', models.TextField(blank=True, null=True, verbose_name="Rector's Resolution")),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation Date')),
                ('last_change_date', models.DateTimeField(auto_now=True, verbose_name='Last Change Date')),
                ('document_file', models.FileField(blank=True, null=True, upload_to='incoming_doc_files', verbose_name='Document File')),
                ('responsible_people', models.ManyToManyField(blank=True, to='user_profiles.profile', verbose_name='Responsible People')),
            ],
        ),
        migrations.CreateModel(
            name='PersonOpinionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opinion', models.TextField(blank=True, null=True, verbose_name='Opinion')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incoming_log.incominglogmodel')),
                ('profile_owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user_profiles.profile')),
            ],
        ),
    ]
