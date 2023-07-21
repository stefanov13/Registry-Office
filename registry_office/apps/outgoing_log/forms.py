from django import forms
from .models import OutgoingLogModel

class CreateOutgoingLogForm(forms.ModelForm):
    class Meta:
        model = OutgoingLogModel
        fields = ('title', 'recipient', 'document_img')

    