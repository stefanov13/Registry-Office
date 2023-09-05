from django import forms
from django.utils.translation import gettext_lazy as _
from . import models


# class CreateIncomingLogForm(forms.ModelForm):
#     class Meta:
#         model = models.IncomingLogModel
#         fields = ['log_num', 'title', 'responsible_people', 'document_file']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.__gen_next_log_num()

#     def __gen_next_log_num(self):
#         last_instance = models.IncomingLogModel.objects.order_by('-pk').first()
#         last_log_num = last_instance.log_num

#         if not last_instance.log_num.isdigit():
#             last_log_num = last_instance.log_num[:-1]

#         self.instance.log_num = int(last_log_num) + 1 if last_instance else 1

class EditIncomingLogForm(forms.ModelForm):
    opinion = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
        label=_('Opinion')
    )
    
    class Meta:
        model = models.IncomingLogModel
        fields = '__all__'

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
