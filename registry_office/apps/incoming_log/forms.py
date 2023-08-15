from django import forms
from .models import IncomingLogModel
from django.utils.translation import gettext_lazy as _

class EditIncomingLogForm(forms.ModelForm):
    opinion = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
        label=_('Opinion')
    )
    class Meta:
        model = IncomingLogModel
        exclude = ['category']

class EditIncomingLogOpinionForm(EditIncomingLogForm):
    class Meta:
        model = IncomingLogModel
        fields = ['opinion']

class DeleteIncomingLogForm(forms.ModelForm):
    class Meta:
        model = IncomingLogModel
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
