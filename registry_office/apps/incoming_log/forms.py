from django import forms
from django.utils.translation import gettext_lazy as _
from . import models


class EditIncomingLogForm(forms.ModelForm):
    opinion = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
        label=_('Opinion')
    )
    
    class Meta:
        model = models.IncomingLogModel
        exclude = ['category']

class EditIncomingLogOpinionForm(EditIncomingLogForm):
    class Meta:
        model = models.IncomingLogModel
        fields = ['opinion']

class DeleteIncomingLogForm(forms.ModelForm):
    class Meta:
        model = models.IncomingLogModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_disabled_fields()

    def save(self, commit=True):
        if commit:
            self.instance.delete()
            
        return self.instance

    def __set_disabled_fields(self):
        for field in self.fields.values():
            field.widget.attrs['disabled'] = True
            field.required = False

class EditPersonOpinionForm(forms.ModelForm):
    class Meta:
        model = models.PersonOpinionModel
        fields = ['opinion']

class DeletePersonOpinionForm(forms.ModelForm):
    class Meta:
        model = models.PersonOpinionModel
        fields = ['opinion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_disabled_fields()

    def save(self, commit=True):
        if commit:
            self.instance.delete()
            
        return self.instance

    def __set_disabled_fields(self):
        for field in self.fields.values():
            field.widget.attrs['disabled'] = True
            field.required = False
