from django import forms
from .models import IncomingLogModel
from django.utils.translation import gettext_lazy as _

class EditIncomingLogForm(forms.ModelForm):
    opinion = forms.CharField(
        required=False,
        widget=forms.Textarea,
    )
    class Meta:
        model = IncomingLogModel
        exclude = ['opinions',]
