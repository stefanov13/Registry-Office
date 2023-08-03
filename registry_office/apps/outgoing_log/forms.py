from django import forms
from .models import OutgoingLogModel
from django.utils.translation import gettext_lazy as _
from core.profile_name_choices import full_profile_name

class CreateOutgoingLogForm(forms.ModelForm):
    # signatory_profile = forms.ChoiceField(choices=(), label=_('Signatory Profile'))
    class Meta:
        model = OutgoingLogModel
        fields = '__all__' # ('title', 'recipient', 'signatory_profile', 'document_img')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.fields['signatory_profile'].choices = full_profile_name()


class EditOutgoingLogForm(forms.ModelForm):
    # NOT_SPECIFIED_CHOICE = 'Is Not Specified'
    # signatory_profile = forms.ChoiceField(choices=full_profile_name(), label=_('Signatory Profile'))
    class Meta:
        model = OutgoingLogModel
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     # Set the initial value for 'signatory_profile' field when editing the record
    #     instance = kwargs.get('instance')
    #     if instance:
    #         initial_value = (f'{instance.signatory_name} {instance.signatory_position}',)
    #         if self.NOT_SPECIFIED_CHOICE in initial_value[0]:
    #             initial_value = (self.NOT_SPECIFIED_CHOICE,)
    #         self.fields['signatory_profile'].initial = initial_value

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
