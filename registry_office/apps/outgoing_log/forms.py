from django import forms
from .models import OutgoingLogModel

class CreateOutgoingLogForm(forms.ModelForm):
    model = OutgoingLogModel
    fields = '__all__'
    