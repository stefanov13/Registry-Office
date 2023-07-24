from django import forms
from .models import OutgoingLogModel
from core.profile_name_choices import full_profile_name

class CreateOutgoingLogForm(forms.ModelForm):
    custom_choice_field = forms.ChoiceField(choices=())
    class Meta:
        model = OutgoingLogModel
        fields = ('title', 'recipient', 'custom_choice_field', 'document_img')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['custom_choice_field'].choices = full_profile_name()


class EditOutgoingLogForm(forms.ModelForm):
    class Meta:
        model = OutgoingLogModel
        fields = ('title', 'recipient', 'document_img')

class DeleteOutgoingLogForm(forms.ModelForm):
    class Meta:
        model = OutgoingLogModel
        fields = ('title', 'recipient', 'document_img')
