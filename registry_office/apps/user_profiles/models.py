from django.db import models
from django.core import validators
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core.validators import name_cyrillic_letters_and_hyphens_validator, position_field_validator

# Create your models here.

UserModel = get_user_model()


class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 50
    LAST_NAME_MAX_LENGTH = 50
    POSITION_MAX_LENGTH = 70
    MIN_LENGTH = 2

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=[
            validators.MinLengthValidator(
                MIN_LENGTH,
                'Името трябва да съдържа поне 2 букви',
            ),
            name_cyrillic_letters_and_hyphens_validator,
        ],
        blank=False,
        null=False,
        verbose_name=_('First Name'),
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=[
            validators.MinLengthValidator(
                MIN_LENGTH,
                'Фамилията трябва да съдържа поне 2 букви',
            ),
            name_cyrillic_letters_and_hyphens_validator,
        ],
        blank=False,
        null=False,
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
