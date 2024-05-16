from django import forms
from .models import GeneralContractsLogModel, ContractTypesModel
from django.utils.translation import gettext_lazy as _

class EditContractsLogForm(forms.ModelForm):
    class Meta:
        model = GeneralContractsLogModel
        exclude = ['creator_user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[
            'concerned_employees'
        ].queryset = self.fields[
            'concerned_employees'
        ].queryset.order_by('pk')

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

class DeleteContractTypesForm(forms.ModelForm):
    class Meta:
        model = ContractTypesModel
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
