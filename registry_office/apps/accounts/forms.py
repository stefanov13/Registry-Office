from django.contrib.auth import get_user_model, forms as auth_forms
from django import forms
from django.core import validators
from ..user_profiles.models import Profile
from core.validators import name_cyrillic_letters_and_hyphens_validator, position_field_validator


UserModel = get_user_model()

class RegisterUserForm(auth_forms.UserCreationForm):
    FIRST_NAME_MAX_LENGTH = 50
    LAST_NAME_MAX_LENGTH = 50
    POSITION_MAX_LENGTH = 70

    first_name = forms.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        required=True,
        validators=(validators.MinLengthValidator(2, 'Името трябва да съдържа поне 2 букви'), name_cyrillic_letters_and_hyphens_validator),
        )
    
    last_name = forms.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        required=True,
        validators=(validators.MinLengthValidator(2, 'Името трябва да съдържа поне 2 букви'), name_cyrillic_letters_and_hyphens_validator),
    )

    position = forms.CharField(
        max_length=POSITION_MAX_LENGTH,
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
            owner=user,
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

class EditUserForm(forms.ModelForm):
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

    class Meta:
        model = UserModel
        fields = ['email',]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        try:
            profile_instance = instance.profile
            kwargs['initial'] = {
                'first_name': profile_instance.first_name,
                'last_name': profile_instance.last_name,
                'position': profile_instance.position,
            }
        except Profile.DoesNotExist:
            kwargs['initial'] = {
                'first_name': '',
                'last_name': '',
                'position': '',
            }
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        # Save both models when the form is saved
        current_user = super().save(commit=False)
        current_user.save()

        profile, created = Profile.objects.get_or_create(owner=current_user)
        profile.first_name = self.cleaned_data['first_name']
        profile.last_name = self.cleaned_data['last_name']
        profile.position = self.cleaned_data['position']
        profile.save()

        return current_user
