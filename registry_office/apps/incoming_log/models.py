from django.db import models
from django.db.models import Max
from django.core import validators
from django.utils.translation import gettext_lazy as _

# Create your models here.

class IncomingLogModel(models.Model):
    LOGS_NUM_MAX_LENGTH = 15
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





    def save(self, *args, **kwargs):
        if not self.log_num:
            # Auto-generate the log_num value on first save
            last_log_num = IncomingLogModel.objects.aggregate(Max('log_num'))['log_num__max']
            next_log_num = 1 if last_log_num is None else int(last_log_num[4:]) + 1
            self.log_num = f'ABC-{next_log_num}'

        super().save(*args, **kwargs)