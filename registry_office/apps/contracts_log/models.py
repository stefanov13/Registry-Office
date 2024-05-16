from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
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
    TITLE_MIN_LENGTH = 2
    TITLE_MAX_LENGTH = 200
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

    creator_user = models.CharField(
        max_length=CREATOR_USER_MAX_LENGTH,
        blank=False,
        null=False,
        verbose_name=_('Creator User')
    )

    first_document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='gen_contracts_doc_files',
        verbose_name=_('First Document File'),
    )

    second_document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='gen_contracts_doc_files',
        verbose_name=_('Second Document File'),
    )

    third_document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='gen_contracts_doc_files',
        verbose_name=_('Third Document File'),
    )

    # def clean(self):
    #     super().clean()

    #     self.current_year = timezone.now().year

    #     same_value_current_year = GeneralContractsLogModel.objects.filter(
    #         creation_date__year=self.current_year,
    #         log_num=self.log_num,
    #         sub_log_num=self.sub_log_num
    #     ).exclude(
    #         pk=self.pk
    #     ).exists()

    #     if same_value_current_year:
    #         raise ValidationError(
    #             _('Cannot have duplicate log numbers in the same year.')
    #         ) # 'В регистъра не може да има два еднакви номера в една година'

    def save(self, *args, **kwargs):
        if not self.log_num:
            # Auto-generate the log_num value on first save
            self.current_year = timezone.now().year
            # last_instance = GeneralContractsLogModel.objects.order_by('-creation_date__date', '-log_num').first()
            last_instance = GeneralContractsLogModel.objects.filter(
                creation_date__year=self.current_year
            ).order_by('-log_num').first()
            
            if last_instance and last_instance.creation_date.year == self.current_year:
                last_log_num = last_instance.log_num
            else:
                last_log_num = 0

            self.log_num = last_log_num + 1

        super().save(*args, **kwargs)

class EducationContractsLogModel(models.Model):
    TITLE_MIN_LENGTH = 2
    TITLE_MAX_LENGTH = 200
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

    creator_user = models.CharField(
        max_length=CREATOR_USER_MAX_LENGTH,
        blank=False,
        null=False,
        verbose_name=_('Creator User')
    )

    first_document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='training_contracts_doc_files',
        verbose_name=_('First Document File'),
    )

    second_document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='training_contracts_doc_files',
        verbose_name=_('Second Document File'),
    )

    third_document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='training_contracts_doc_files',
        verbose_name=_('Third Document File'),
    )

    # def clean(self):
    #     super().clean()

    #     self.current_year = timezone.now().year

    #     same_value_current_year = EducationContractsLogModel.objects.filter(
    #         creation_date__year=self.current_year,
    #         log_num=self.log_num,
    #         sub_log_num=self.sub_log_num
    #     ).exclude(
    #         pk=self.pk
    #     ).exists()

    #     if same_value_current_year:
    #         raise ValidationError(
    #             _('Cannot have duplicate log numbers in the same year.')
    #         ) # 'В регистъра не може да има два еднакви номера в една година'

    def save(self, *args, **kwargs):
        if not self.log_num:
            # Auto-generate the log_num value on first save
            self.current_year = timezone.now().year
            # last_instance = EducationContractsLogModel.objects.order_by('-creation_date__date', '-log_num').first()
            last_instance = EducationContractsLogModel.objects.filter(
                creation_date__year=self.current_year
            ).order_by('-log_num').first()

            if last_instance and last_instance.creation_date.year == self.current_year:
                last_log_num = last_instance.log_num
            else:
                last_log_num = 0

            self.log_num = last_log_num + 1

        super().save(*args, **kwargs)

class FreelanceContractsLogModel(models.Model):
    TITLE_MIN_LENGTH = 2
    TITLE_MAX_LENGTH = 200
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

    creator_user = models.CharField(
        max_length=CREATOR_USER_MAX_LENGTH,
        blank=False,
        null=False,
        verbose_name=_('Creator User')
    )

    first_document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='freelance_contracts_doc_files',
        verbose_name=_('First Document File'),
    )

    second_document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='freelance_contracts_doc_files',
        verbose_name=_('Second Document File'),
    )

    third_document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='freelance_contracts_doc_files',
        verbose_name=_('Third Document File'),
    )

    # def clean(self):
    #     super().clean()

    #     self.current_year = timezone.now().year

    #     same_value_current_year = FreelanceContractsLogModel.objects.filter(
    #         creation_date__year=self.current_year,
    #         log_num=self.log_num,
    #         sub_log_num=self.sub_log_num
    #     ).exclude(
    #         pk=self.pk
    #     ).exists()

    #     if same_value_current_year:
    #         raise ValidationError(
    #             _('Cannot have duplicate log numbers in the same year.')
    #         ) # 'В регистъра не може да има два еднакви номера в една година'

    def save(self, *args, **kwargs):
        if not self.log_num:
            # Auto-generate the log_num value on first save
            self.current_year = timezone.now().year
            # last_instance = FreelanceContractsLogModel.objects.order_by('-creation_date__date', '-log_num').first()
            last_instance = FreelanceContractsLogModel.objects.filter(
                creation_date__year=self.current_year
            ).order_by('-log_num').first()

            if last_instance and last_instance.creation_date.year == self.current_year:
                last_log_num = last_instance.log_num
            else:
                last_log_num = 0

            self.log_num = last_log_num + 1

        super().save(*args, **kwargs)

class FreelanceLectureContractsLogModel(models.Model):
    TITLE_MIN_LENGTH = 2
    TITLE_MAX_LENGTH = 200
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

    creator_user = models.CharField(
        max_length=CREATOR_USER_MAX_LENGTH,
        blank=False,
        null=False,
        verbose_name=_('Creator User')
    )

    first_document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='freelance_lecture_contracts_doc_files',
        verbose_name=_('First Document File'),
    )

    second_document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='freelance_lecture_contracts_doc_files',
        verbose_name=_('Second Document File'),
    )

    third_document_file = models.FileField(
        blank=True,
        null=True,
        upload_to='freelance_lecture_contracts_doc_files',
        verbose_name=_('Third Document File'),
    )

    # def clean(self):
    #     super().clean()

    #     self.current_year = timezone.now().year

    #     same_value_current_year = FreelanceLectureContractsLogModel.objects.filter(
    #         creation_date__year=self.current_year,
    #         log_num=self.log_num,
    #         sub_log_num=self.sub_log_num
    #     ).exclude(
    #         pk=self.pk
    #     ).exists()

    #     if same_value_current_year:
    #         raise ValidationError(
    #             _('Cannot have duplicate log numbers in the same year.')
    #         ) # 'В регистъра не може да има два еднакви номера в една година'

    def save(self, *args, **kwargs):
        if not self.log_num:
            # Auto-generate the log_num value on first save
            self.current_year = timezone.now().year
            # last_instance = FreelanceLectureContractsLogModel.objects.order_by('-creation_date__date', '-log_num').first()
            last_instance = FreelanceLectureContractsLogModel.objects.filter(
                creation_date__year=self.current_year
            ).order_by('-log_num').first()

            if last_instance and last_instance.creation_date.year == self.current_year:
                last_log_num = last_instance.log_num
            else:
                last_log_num = 0

            self.log_num = last_log_num + 1

        super().save(*args, **kwargs)
