from django import forms
from .models import OutgoingLogModel
from django.utils.translation import gettext_lazy as _

class CreateOutgoingLogForm(forms.ModelForm):
    class Meta:
        model = OutgoingLogModel
        fields = ['title', 'recipient', 'signatory_employee_id', 'document_file']

class EditOutgoingLogForm(forms.ModelForm):
    class Meta:
        model = OutgoingLogModel
        fields = '__all__'

class DeleteOutgoingLogForm(forms.ModelForm):
    class Meta:
        model = OutgoingLogModel
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
