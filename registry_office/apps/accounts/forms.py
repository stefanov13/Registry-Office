from django.contrib.auth import get_user_model, forms as auth_forms
from django import forms
from ..user_profiles.models import Profile

UserModel = get_user_model()

class RegisterUserForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        required=True,
        )
    
    last_name = forms.CharField(
        max_length=100,
        required=True,
    )

    position = forms.CharField(
        max_length=100,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__remove_help_text()

    def save(self, commit=True):
        user = super().save(commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            position=self.cleaned_data['position'],
            user=user,
        )
        if commit:
            profile.save()

    def __remove_help_text(self):
        for field_name in ['email', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)
