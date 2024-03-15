from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def position_field_validator(value):
    value = value.strip()
    pattern = r'^([А-Яа-яA-Za-z\.?\s?\-?\"?]+)$'

    if not re.match(pattern, value):
        raise ValidationError(
            _('The text must contain only lower or uppercase letters, dashes, dots, spaces and quotes!')
        )  # 'Текстът трябва да съдържа само главни и малки букви, тирета, точки и кавички!'
    

def name_cyrillic_letters_and_hyphens_validator(value):
    value = value.strip()
    pattern = r'^([А-Я]{1}[а-я]+)(\s*\-\s*[А-Я]{1}[а-я]+)*$'

    if not re.match(pattern, value):
        raise ValidationError(
            _('The first letter of the name must be capitalized and must contain only Cyrillic letters and dashes!')
        )  # 'Името трябва задължително да започва с главна булва и да съдържа само български букви и тирета!'
 