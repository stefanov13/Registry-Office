from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _
from core.profile_name_choices import FullProfileName

# Create your models here.



class OutgoingLogModel(models.Model):
    log_num = models.IntegerField(
        blank=False,
        null=False, 
        unique=True, 
        editable=False,
        verbose_name=(_('Log\'s number'))
    )

    title = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        validators=[validators.MinLengthValidator(2, 'Полето трябва да съдържа поне 2 букви')],
        verbose_name=(_('Title')),
    )

    recipient = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        validators=[validators.MinLengthValidator(2, 'Полето трябва да съдържа поне 2 букви')],
        verbose_name=(_('Recipient')),
    )

    signatory_name = models.CharField(
        max_length=70,   #FullProfileName.max_length()
        blank=False,
        null=False,
        choices=FullProfileName.choices,
        default=(_('Not Present'))
    )

    signatory_position = models.CharField(
        max_length=70,
        blank=False,
        null=False,
    )

    creation_date = models.DateTimeField(
        auto_now=True,
    )

    document_img = models.ImageField(
        blank=True,
        null=True,
        upload_to='outgoing_doc_img',
        
    )

    def save(self, *args, **kwargs):
        if not self.log_num:
            # Auto-generate the log_num value on first save
            last_instance = OutgoingLogModel.objects.order_by('-log_num').first()
            self.log_num = (last_instance.log_num + 1) if last_instance else 1

        super().save(*args, **kwargs)