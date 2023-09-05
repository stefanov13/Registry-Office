from django.db import models
from django.core import validators
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ..user_profiles.models import Profile
from core.register_category_types_choices import CategoryTypesChoices

# Create your models here.

class IncomingLogModel(models.Model):
    LOGS_NUM_MAX_LENGTH = 15
    CATEGORY_MAX_LENGTH = 1
    TITLE_MIN_LENGTH = 2
    TITLE_MAX_LENGTH = 150
    
    log_num = models.CharField(
        max_length=LOGS_NUM_MAX_LENGTH,
        blank=False,
        null=False, 
        unique=True,
        verbose_name=_('Log\'s number')
    )

    category = models.CharField(
        max_length=CategoryTypesChoices.max_length(),
        blank=True,
        null=True,
        choices=CategoryTypesChoices.choices(),
        verbose_name=_('Category'),
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

    responsible_people = models.ManyToManyField(
        Profile,
        blank=True,
        verbose_name=_('Responsible People'),
    )

    creation_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Creation Date'),
    )

    last_change_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Change Date'),
    )

    document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='incoming_doc_files',
        verbose_name=_('Document File'),
    )

    def save(self, *args, **kwargs):
        if not self.log_num:
            # Auto-generate the log_num value on first save
            last_instance = IncomingLogModel.objects.order_by('-log_num').first()
            self.log_num = int(last_instance.log_num) + 1 if last_instance else 1

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

    profile_owner = models.ForeignKey(
        Profile,
        on_delete=models.DO_NOTHING,
    )

    document = models.ForeignKey(
        IncomingLogModel,
        on_delete=models.CASCADE,
    )
