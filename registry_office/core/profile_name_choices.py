from enum import Enum
from .mixins.choices_mixin import ChoicesMixin
from apps.user_profiles.models import Profile


class FullProfileName:
    profiles = Profile.objects.all()
    choices = [(f'{p.first_name} {p.last_name}', f'{p.first_name} {p.last_name}') for p in profiles]
    

    # @property
    # def full_names(self):
    #     return [f'{profile.first_name} {profile.last_name}' for profile in self.profiles]
