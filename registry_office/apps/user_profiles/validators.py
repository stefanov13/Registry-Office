from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def lowercase_cyrillic_letters_and_hyphens_validator(value):
    value = value.strip()
    pattern = r'^([а-я]+)(\s*\-\s*[а-я]+)*$'
    if not re.match(pattern, value):
        raise ValidationError(_('The text must contain only lowercase Cyrillic letters and dashes!'))  # 'Текстът трябва да съдържа само малки български букви и тирета!'
    

def name_cyrillic_letters_and_hyphens_validator(value):
    value = value.strip()
    pattern = r'^([А-Я]{1}[а-я]+)(\s*\-\s*[А-Я]{1}[а-я]+)*$'
    if not re.match(pattern, value):
        raise ValidationError(_('The first letter of the name must be capitalized and must contain only Cyrillic letters and dashes!'))  # 'Името трябва задължително да започва с главна булва и да съдържа само български букви и тирета!'
