from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ..user_profiles.models import Profile, EmployeePositionsModel


# from core.register_category_types_choices import CategoryTypesChoices

# Create your models here.

class IncomingLogModel(models.Model):
    CATEGORY_MAX_LENGTH = 1
    TITLE_MIN_LENGTH = 2
    TITLE_MAX_LENGTH = 150
    CREATOR_USER_MAX_LENGTH = 150
    
    log_num = models.IntegerField(
        blank=False,
        null=False,
        verbose_name=_('Log\'s number'),
    )

    sub_log_num = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_('Sub Log\'s number'),
    )

    # category = models.CharField(
    #     max_length=CategoryTypesChoices.max_length(),
    #     blank=True,
    #     null=True,
    #     choices=CategoryTypesChoices.choices(),
    #     verbose_name=_('Category'),
    # )

    creation_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Creation Date'),
    )

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        blank=False,
        null=False,
        validators=[
            validators.MinLengthValidator(
            TITLE_MIN_LENGTH, 
            'Полето трябва да съдържа поне 2 букви',
            ),
        ],
        verbose_name=_('Title'),
    )

    rectors_resolution = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Rector\'s Resolution'),
    )

    # responsible_people = models.ManyToManyField(
    #     Profile,
    #     blank=True,
    #     verbose_name=_('Responsible People'),
    # )

    concerned_employees = models.ManyToManyField(
        EmployeePositionsModel,
        blank=True,
        verbose_name=_('Responsible Employees'),
    )

    creator_user = models.CharField(
        max_length=CREATOR_USER_MAX_LENGTH,
        blank=False,
        null=False,
        verbose_name=_('Creator User')
    )

    last_change_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Change Date'),
    )

    first_document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='incoming_doc_files',
        verbose_name=_('First Document File'),
    )

    second_document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='incoming_doc_files',
        verbose_name=_('Second Document File'),
    )

    third_document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='incoming_doc_files',
        verbose_name=_('Third Document File'),
    )

    def clean(self):
        super().clean()

        self.current_year = timezone.now().year

        same_value_current_year = IncomingLogModel.objects.filter(
            creation_date__year=self.current_year, log_num=self.log_num, sub_log_num=self.sub_log_num
        ).exclude(
            pk=self.pk
        ).exists()

        if same_value_current_year:
            raise ValidationError(
                _('Cannot have duplicate log numbers in the same year.')
            ) # 'В регистъра не може да има два еднакви номера в една година'

    def save(self, *args, **kwargs):
        if not self.log_num:
            # Auto-generate the log_num value on first save
            last_instance = IncomingLogModel.objects.order_by('-creation_date__date', '-log_num').first()

            if last_instance and last_instance.creation_date.year == self.current_year:
                last_log_num = last_instance.log_num
            else:
                last_log_num = 0

            self.log_num = last_log_num + 1

        super().save(*args, **kwargs)

    """By old SRS"""

    # def save(self, *args, **kwargs):
    #     selected_category = self.category.replace('_', '-')

    #     if not self.log_num:
    #         # Auto-generate the log_num value on first save
    #         last_log_num = IncomingLogModel.objects.order_by('-pk').first()
            
    #         next_log_num = 1 if last_log_num is None else int(last_log_num.log_num.split('-')[-1]) + 1
    #         self.log_num = f'{selected_category}-{next_log_num}'

    #     super().save(*args, **kwargs)

class PersonOpinionModel(models.Model):
    opinion = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Opinion'),
    )

    creation_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Creation Date'),
    )

    last_change_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Change Date'),
    )

    profile_owner = models.ForeignKey(
        Profile,
        on_delete=models.DO_NOTHING,
    )

    document = models.ForeignKey(
        IncomingLogModel,
        on_delete=models.CASCADE,
    )
