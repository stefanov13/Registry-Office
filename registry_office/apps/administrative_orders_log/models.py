from django.db import models
from django.core import validators
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ..user_profiles.models import EmployeePositionsModel


class AdministrativeOrdersLogModel(models.Model):
    LOG_NUM_MAX_LENGTH = 7
    TITLE_MIN_LENGTH = 2
    TITLE_MAX_LENGTH = 200
    PUBLISHER_MIN_LENGTH = 2
    PUBLISHER_MAX_LENGTH = 100
    
    log_num = models.CharField(
        max_length=LOG_NUM_MAX_LENGTH,
        blank=False,
        null=False,
        verbose_name=_('Log\'s number')
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

    publisher = models.CharField(
        max_length=PUBLISHER_MAX_LENGTH,
        blank=True,
        null=True,
        validators=[
            validators.MinLengthValidator(
            PUBLISHER_MIN_LENGTH, 
            'Полето трябва да съдържа поне 2 букви',
            )
        ],
        verbose_name=_('Publisher'),
    )

    responsible_employees = models.ManyToManyField(
        EmployeePositionsModel,
        on_delete=models.DO_NOTHING,
        verbose_name=_('Responsible Employees'),
    )

    document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='outgoing_doc_files',
        verbose_name=_('Document File'),
    )

    def save(self, *args, **kwargs):
        if not self.log_num:
            # Auto-generate the log_num value on first save
            last_instance = AdministrativeOrdersLogModel.objects.order_by('-creation_date', '-log_num').first()

            current_year = timezone.now().year

            if last_instance and last_instance.creation_date.year == current_year:
                last_log_num = last_instance.log_num
            else:
                last_log_num = '0'

            last_log_num = last_log_num.split('-')[0]
            numeric_part = ''.join(filter(str.isdigit, last_log_num))

            self.log_num = int(numeric_part) + 1

        # file_type, encoding = mimetypes.guess_type(self.document_file.path)

        super().save(*args, **kwargs)
