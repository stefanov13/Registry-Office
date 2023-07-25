from django import forms
from .models import OutgoingLogModel
from django.utils.translation import gettext_lazy as _
from core.profile_name_choices import full_profile_name

class CreateOutgoingLogForm(forms.ModelForm):
    signatory_profile = forms.ChoiceField(choices=(), label=_('Signatory Profile'))
    class Meta:
        model = OutgoingLogModel
        fields = ('title', 'recipient', 'signatory_profile', 'document_img')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['signatory_profile'].choices = full_profile_name()


class EditOutgoingLogForm(forms.ModelForm):
    signatory_profile = forms.ChoiceField(choices=full_profile_name(), label=_('Signatory Profile'))
    class Meta:
        model = OutgoingLogModel
        fields = ('title', 'recipient', 'signatory_profile', 'document_img')

class DeleteOutgoingLogForm(forms.ModelForm):
    class Meta:
        model = OutgoingLogModel
        fields = ('title', 'recipient')
