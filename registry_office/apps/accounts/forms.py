from django.contrib.auth import get_user_model, forms as auth_forms
from django import forms
from django.core import validators
from ..user_profiles.models import Profile
from ..user_profiles.validators import name_cyrillic_letters_and_hyphens_validator, position_field_validator

UserModel = get_user_model()

class RegisterUserForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        required=True,
        validators=(validators.MinLengthValidator(2, 'Името трябва да съдържа поне 2 букви'), name_cyrillic_letters_and_hyphens_validator),
        )
    
    last_name = forms.CharField(
        max_length=100,
        required=True,
        validators=(validators.MinLengthValidator(2, 'Името трябва да съдържа поне 2 букви'), name_cyrillic_letters_and_hyphens_validator),
    )

    position = forms.CharField(
        max_length=100,
        required=True,
        validators=(validators.MinLengthValidator(2, 'Длъжността трябва да съдържа поне 2 букви'), position_field_validator),
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

        return user

    def __remove_help_text(self):
        for field_name in ['email', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)
