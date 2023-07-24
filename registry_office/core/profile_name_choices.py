# from enum import Enum
# from .mixins.choices_mixin import ChoicesMixin
from django.utils.translation import gettext_lazy as _
from apps.user_profiles.models import Profile



def full_profile_name():
    try:
        profiles = Profile.objects.all()
        choices = [(f'{p.first_name} {p.last_name} {p.position}', f'{p.first_name} {p.last_name} {p.position}') for p in profiles]
        choices += [(_('Not Present'), _('Not Present'))]
    except:
        choices = [(_('Not Present'), _("Not Present"))]
    return choices
