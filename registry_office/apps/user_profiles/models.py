from django.db import models
from django.core import validators
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core.validators import name_cyrillic_letters_and_hyphens_validator, position_field_validator

# Create your models here.

UserModel = get_user_model()


class Profile(models.Model):
    first_name = models.CharField(
        max_length=100,
        validators=[validators.MinLengthValidator(2, 'Името трябва да съдържа поне 2 букви'), name_cyrillic_letters_and_hyphens_validator],
        blank=False,
        null=False,
        verbose_name=_('First Name'),
    )

    last_name = models.CharField(
        max_length=100,
        validators=[validators.MinLengthValidator(2, 'Фамилията трябва да съдържа поне 2 букви'), name_cyrillic_letters_and_hyphens_validator],
        blank=False,
        null=False,
        verbose_name=_('Last Name'),
    )

    position = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        validators=[validators.MinLengthValidator(2, 'Длъжността трябва да съдържа поне 2 букви'), position_field_validator],
        verbose_name=_('Position'),
    )

    owner = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )
