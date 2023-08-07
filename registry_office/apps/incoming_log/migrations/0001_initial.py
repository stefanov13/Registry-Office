# Generated by Django 4.2.3 on 2023-08-05 20:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


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
                ('log_num', models.CharField(editable=False, max_length=80, unique=True, verbose_name="Log's number")),
                ('category', models.CharField(choices=[('РД', 'Ръководна дейност'), ('УД', 'Учебна дейност'), ('ФД', 'Факултетна дейност'), ('ФДСИ', 'Факултетна дейност - "Сценични изкуства"'), ('ФДЕИ', 'Факултетна дейност - "Екранни изкуства"'), ('НИД', 'Научна и издателска дейност'), ('ХТД', 'Художествено - творческа дейност'), ('ХТД_УДТ', 'Худож. - творч. д-ност - Учебен драматичен театър'), ('ХТД_УКТ', 'Худож. - творч. д-ност - Учебен куклен театър'), ('ХТД_УАВК', 'Худож. - творч. д-ност - Учебен аудио визуален комплекс'), ('МС', 'Международно сътрудничество'), ('ПД', 'Проектна дейност'), ('ФСД', 'Финансово  - счетоводна дейност'), ('АПД', 'Административно - правна дейност'), ('ЧР', 'Човешки ресурси'), ('БТ', 'Безопасност на труда'), ('КС', 'Капитално строителство'), ('БД', 'Библиотечна дейност'), ('СС', 'Студентски съвет')], max_length=55, verbose_name='Category')),
                ('title', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Полето трябва да съдържа поне 2 букви')], verbose_name='Title')),
                ('rectors_resolution', models.TextField(blank=True, null=True, verbose_name="Rector's resolution")),
                ('document_img', models.ImageField(blank=True, null=True, upload_to='outgoing_doc_img', verbose_name='Document Image')),
                ('responsible_persons', models.ManyToManyField(blank=True, to='user_profiles.profile', verbose_name='Responsible persons')),
            ],
        ),
        migrations.CreateModel(
            name='PersonOpinion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opinion', models.TextField(blank=True, null=True, verbose_name='Opinion')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incoming_log.incominglogmodel')),
                ('profile_owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user_profiles.profile')),
            ],
        ),
    ]
