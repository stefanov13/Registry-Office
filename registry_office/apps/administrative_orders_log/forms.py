from django import forms
from .models import AdministrativeOrdersLogModel
from django.utils.translation import gettext_lazy as _


class EditAdministrativeOrdersLogForm(forms.ModelForm):
    class Meta:
        model = AdministrativeOrdersLogModel
        exclude = ['creator_user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[
            'concerned_employees'
        ].queryset = self.fields[
            'concerned_employees'
        ].queryset.order_by('pk')

class DeleteAdministrativeOrdersLogForm(forms.ModelForm):
    class Meta:
        model = AdministrativeOrdersLogModel
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
