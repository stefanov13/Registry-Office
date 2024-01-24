from django import forms
from .models import GeneralContractsLogModel
from django.utils.translation import gettext_lazy as _


class DeleteContractsLogForm(forms.ModelForm):
    class Meta:
        model = GeneralContractsLogModel
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
