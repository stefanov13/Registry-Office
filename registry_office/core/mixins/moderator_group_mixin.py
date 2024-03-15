from django.contrib.auth.mixins import AccessMixin
from django.http import Http404

class GroupRequiredMixin(AccessMixin):
    allowed_groups = []

    def dispatch(self, request, *args, **kwargs):
        user_groups = set(request.user.groups.values_list('name', flat=True))
        rights = [
                user_groups.intersection(set(self.allowed_groups)),
                request.user.is_superuser,
                request.user.is_staff
            ]

        if not rights:
            raise Http404()
        
        return super().dispatch(request, *args, **kwargs)
