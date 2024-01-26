from django.db import models
from django.core import validators
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ..user_profiles.models import EmployeePositionsModel


class ContractTypesModel(models.Model):
    CONTRACT_TYPE_MIN_LENGTH = 2
    CONTRACT_TYPE_MAX_LENGTH = 200

    contract_type = models.CharField(
        max_length=CONTRACT_TYPE_MAX_LENGTH,
        blank=False,
        null=False,
        validators=[
            validators.MinLengthValidator(
            CONTRACT_TYPE_MIN_LENGTH, 
            'Полето трябва да съдържа поне 2 букви',
            )
        ],
        verbose_name=_('Contract Type'),
    )

    def __str__(self):
        return self.contract_type

class GeneralContractsLogModel(models.Model):
    LOG_NUM_MAX_LENGTH = 7
    TITLE_MIN_LENGTH = 2
    TITLE_MAX_LENGTH = 200
    
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

    contract_type = models.ForeignKey(
        ContractTypesModel,
        on_delete=models.DO_NOTHING,
        verbose_name=_('Contract type'),
    )

    concerned_employees = models.ManyToManyField(
        EmployeePositionsModel,
        blank=True,
        verbose_name=_('Concerned Employees'),
    )

    document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='gen_contracts_doc_files',
        verbose_name=_('Document File'),
    )

    def save(self, *args, **kwargs):
        if not self.log_num:
            # Auto-generate the log_num value on first save
            last_instance = GeneralContractsLogModel.objects.order_by(
                '-creation_date',
                '-log_num',
                ).first()

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

class EducationContractsLogModel(models.Model):
    LOG_NUM_MAX_LENGTH = 7
    TITLE_MIN_LENGTH = 2
    TITLE_MAX_LENGTH = 200
    
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

    contract_type = models.ForeignKey(
        ContractTypesModel,
        on_delete=models.DO_NOTHING,
        verbose_name=_('Contract type'),
    )

    concerned_employees = models.ManyToManyField(
        EmployeePositionsModel,
        blank=True,
        verbose_name=_('Concerned Employees'),
    )

    document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='training_contracts_doc_files',
        verbose_name=_('Document File'),
    )

    def save(self, *args, **kwargs):
        if not self.log_num:
            # Auto-generate the log_num value on first save
            last_instance = EducationContractsLogModel.objects.order_by(
                '-creation_date',
                '-log_num',
                ).first()

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

class FreelanceContractsLogModel(models.Model):
    LOG_NUM_MAX_LENGTH = 7
    TITLE_MIN_LENGTH = 2
    TITLE_MAX_LENGTH = 200
    
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

    contract_type = models.ForeignKey(
        ContractTypesModel,
        on_delete=models.DO_NOTHING,
        verbose_name=_('Contract type'),
    )

    concerned_employees = models.ManyToManyField(
        EmployeePositionsModel,
        blank=True,
        verbose_name=_('Concerned Employees'),
    )

    document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='freelance_contracts_doc_files',
        verbose_name=_('Document File'),
    )

    def save(self, *args, **kwargs):
        if not self.log_num:
            # Auto-generate the log_num value on first save
            last_instance = FreelanceContractsLogModel.objects.order_by(
                '-creation_date',
                '-log_num',
                ).first()

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

class FreelanceLectureContractsLogModel(models.Model):
    LOG_NUM_MAX_LENGTH = 7
    TITLE_MIN_LENGTH = 2
    TITLE_MAX_LENGTH = 200
    
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

    contract_type = models.ForeignKey(
        ContractTypesModel,
        on_delete=models.DO_NOTHING,
        verbose_name=_('Contract type'),
    )

    concerned_employees = models.ManyToManyField(
        EmployeePositionsModel,
        blank=True,
        verbose_name=_('Concerned Employees'),
    )

    document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='freelance_lecture_contracts_doc_files',
        verbose_name=_('Document File'),
    )

    def save(self, *args, **kwargs):
        if not self.log_num:
            # Auto-generate the log_num value on first save
            last_instance = FreelanceLectureContractsLogModel.objects.order_by(
                '-creation_date',
                '-log_num',
                ).first()

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
