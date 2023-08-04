from django.db import models
from django.contrib.auth import get_user_model
from django.core import validators
from django.utils.translation import gettext_lazy as _
from ..user_profiles.models import Profile



class OutgoingLogModel(models.Model):
    TITLE_MIN_LENGTH = 2
    TITLE_MAX_LENGTH = 200
    RECIPIENT_MIN_LENGTH = 2
    RECIPIENT_MAX_LENGTH = 200
    
    log_num = models.IntegerField(
        blank=False,
        null=False, 
        unique=True, 
        editable=False,
        verbose_name=_('Log\'s number')
    )

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        blank=False,
        null=False,
        validators=[validators.MinLengthValidator(TITLE_MIN_LENGTH, 'Полето трябва да съдържа поне 2 букви')],
        verbose_name=_('Title'),
    )

    recipient = models.CharField(
        max_length=RECIPIENT_MAX_LENGTH,
        blank=False,
        null=False,
        validators=[validators.MinLengthValidator(RECIPIENT_MIN_LENGTH, 'Полето трябва да съдържа поне 2 букви')],
        verbose_name=_('Recipient'),
    )

    signatory_profile = models.ForeignKey(
        Profile,
        on_delete=models.DO_NOTHING,
    )
    
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation Date'),
    )

    document_img = models.ImageField(
        blank=True,
        null=True,
        upload_to='outgoing_doc_img',
        verbose_name=_('Document Image'),
    )

    def save(self, *args, **kwargs):
        if not self.log_num:
            # Auto-generate the log_num value on first save
            last_instance = OutgoingLogModel.objects.order_by('-log_num').first()
            self.log_num = (last_instance.log_num + 1) if last_instance else 1

        super().save(*args, **kwargs)
