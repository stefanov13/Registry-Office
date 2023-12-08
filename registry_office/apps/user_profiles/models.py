from django.db import models
from django.core import validators
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core.validators import name_cyrillic_letters_and_hyphens_validator, position_field_validator


UserModel = get_user_model()


class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 50
    LAST_NAME_MAX_LENGTH = 50
    POSITION_MAX_LENGTH = 70
    MIN_LENGTH = 2

    first_name = models.CharField(
        blank=False,
        null=False,
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=[
            validators.MinLengthValidator(
                MIN_LENGTH,
                'Името трябва да съдържа поне 2 букви',
            ),
            name_cyrillic_letters_and_hyphens_validator,
        ],
        verbose_name=_('First Name'),
    )

    last_name = models.CharField(
        blank=False,
        null=False,
        max_length=LAST_NAME_MAX_LENGTH,
        validators=[
            validators.MinLengthValidator(
                MIN_LENGTH,
                'Фамилията трябва да съдържа поне 2 букви',
            ),
            name_cyrillic_letters_and_hyphens_validator,
        ],
        verbose_name=_('Last Name'),
    )

    position = models.CharField(
        max_length=POSITION_MAX_LENGTH,
        blank=False,
        null=False,
        validators=[
            validators.MinLengthValidator(
                MIN_LENGTH,
                'Длъжността трябва да съдържа поне 2 букви',
            ),
            position_field_validator,
        ],
        verbose_name=_('Position'),
    )

    owner = models.OneToOneField(
        UserModel,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.position}'

class EmployeePositionsModel(models.Model):
    EMPLOYEE_POSITION_ID_MAX_LENGTH = 50
    FIRST_NAME_MAX_LENGTH = 50
    LAST_NAME_MAX_LENGTH = 50
    POSITION_MAX_LENGTH = 70
    MIN_LENGTH = 2

    employee_position_id = models.CharField(
        max_length=EMPLOYEE_POSITION_ID_MAX_LENGTH,
        blank=False,
        null=False,
        unique=True,
        validators=[
            validators.MinLengthValidator(
                MIN_LENGTH,
                'The identifier must contain at least 2 symbols', 
                #'Идентификаторът трябва да съдържа поне 2 букви'
            ),
            position_field_validator,
        ],
        verbose_name=_('Position\'s Identifier'),
    )

    first_name = models.CharField(
        blank=True,
        null=True,
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=[
            validators.MinLengthValidator(
                MIN_LENGTH,
                'Името трябва да съдържа поне 2 букви',
            ),
            name_cyrillic_letters_and_hyphens_validator,
        ],
        verbose_name=_('First Name'),
    )

    last_name = models.CharField(
        blank=True,
        null=True,
        max_length=LAST_NAME_MAX_LENGTH,
        validators=[
            validators.MinLengthValidator(
                MIN_LENGTH,
                'Фамилията трябва да съдържа поне 2 букви',
            ),
            name_cyrillic_letters_and_hyphens_validator,
        ],
        verbose_name=_('Last Name'),
    )

    employee_position = models.CharField(
        max_length=POSITION_MAX_LENGTH,
        blank=True,
        null=True,
        validators=[
            validators.MinLengthValidator(
                MIN_LENGTH,
                'Длъжността трябва да съдържа поне 2 букви',
            ),
            position_field_validator,
        ],
        verbose_name=_('Position'),
    )

    employee_department = models.CharField(
        blank=True,
        null=True,
        validators=[
            validators.MinLengthValidator(
                MIN_LENGTH,
                'Department must contain at least 2 symbols', 
                #'Отделът трябва да съдържа поне 2 букви'
            ),
            position_field_validator,
        ],
        verbose_name=_('Department'),
    )

    employee_owner = models.ManyToManyField(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.employee_position_id} {self.first_name} {self.last_name} - {self.employee_position}, {self.employee_department}'
    