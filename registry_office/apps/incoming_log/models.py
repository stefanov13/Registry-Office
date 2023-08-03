from django.db import models
from django.db.models import Max
from django.core import validators
from django.utils.translation import gettext_lazy as _
from ..user_profiles.models import Profile

# Create your models here.

class IncomingLogModel(models.Model):
    LOGS_NUM_MAX_LENGTH = 15
    CATEGORY_MAX_LENGTH = 1
    TITLE_MIN_LENGTH = 2
    TITLE_MAX_LENGTH = 200
    
    log_num = models.CharField(
        max_length=LOGS_NUM_MAX_LENGTH,
        blank=False,
        null=False, 
        unique=True, 
        editable=False,
        verbose_name=_('Log\'s number')
    )

    category = models.CharField(
        max_length=CATEGORY_MAX_LENGTH,
        blank=False,
        null=False,
        
    )

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        blank=False,
        null=False,
        validators=[validators.MinLengthValidator(TITLE_MIN_LENGTH, 'Полето трябва да съдържа поне 2 букви'),],
        verbose_name=_('Title'),
    )

    rectors_resolution = models.TextField(
        blank=True,
        null=True,
    )

    responsible_persons = models.ManyToManyField(
        to=Profile,
        blank=True,
    )

    opinion = models.TextField(
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if not self.log_num:
            # Auto-generate the log_num value on first save
            last_log_num = IncomingLogModel.objects.aggregate(Max('log_num'))['log_num__max']
            next_log_num = 1 if last_log_num is None else int(last_log_num.split('-')[-1]) + 1
            self.log_num = f'ABC-{next_log_num}'

        super().save(*args, **kwargs)
