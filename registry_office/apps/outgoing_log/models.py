from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ..user_profiles.models import EmployeePositionsModel


class OutgoingLogModel(models.Model):
    TITLE_MIN_LENGTH = 2
    TITLE_MAX_LENGTH = 200
    RECIPIENT_MIN_LENGTH = 2
    RECIPIENT_MAX_LENGTH = 200
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
            )
        ],
        verbose_name=_('Title'),
    )

    recipient = models.CharField(
        max_length=RECIPIENT_MAX_LENGTH,
        blank=False,
        null=False,
        validators=[
            validators.MinLengthValidator(
            RECIPIENT_MIN_LENGTH, 
            'Полето трябва да съдържа поне 2 букви',
            )
        ],
        verbose_name=_('Recipient'),
    )

    # signatory_profile = models.ForeignKey(
    #     Profile,
    #     on_delete=models.DO_NOTHING,
    #     verbose_name=_('Signatory Profile'),
    # )

    concerned_employees = models.ForeignKey(
        EmployeePositionsModel,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name=_('Signatory Employee\'s ID'),
    )

    creator_user = models.CharField(
        max_length=CREATOR_USER_MAX_LENGTH,
        blank=False,
        null=False,
        verbose_name=_('Creator User')
    )

    first_document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='outgoing_doc_files',
        verbose_name=_('First Document File'),
    )

    second_document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='outgoing_doc_files',
        verbose_name=_('Second Document File'),
    )
    
    third_document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='outgoing_doc_files',
        verbose_name=_('Third Document File'),
    )

    def clean(self):
        super().clean()

        self.current_year = timezone.now().year

        same_value_current_year = OutgoingLogModel.objects.filter(
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
            last_instance = OutgoingLogModel.objects.order_by('-creation_date__date', '-log_num').first()

            if last_instance and last_instance.creation_date.year == self.current_year:
                last_log_num = last_instance.log_num
            else:
                last_log_num = 0

            self.log_num = last_log_num + 1

        super().save(*args, **kwargs)
