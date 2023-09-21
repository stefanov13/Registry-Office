from django.shortcuts import get_object_or_404
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.http import Http404
from .models import OutgoingLogModel
from .forms import CreateOutgoingLogForm, EditOutgoingLogForm, DeleteOutgoingLogForm
from core.mixins.moderator_group_mixin import GroupRequiredMixin
from core.custom_views.extra_content_create_view import ExtraContentCreateView


class OutgoingLogCreateView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    ExtraContentCreateView
):
    template_name = 'outgoing_log/outgoing-create.html'
    model = OutgoingLogModel
    form_class = CreateOutgoingLogForm
    success_url = reverse_lazy('outgoing-dashboard')

    allowed_groups = ['admin', 'document_controller']

class OutgoingLogDetailsView(
    auth_mixins.LoginRequiredMixin,
    views.DetailView
):
    template_name = 'outgoing_log/outgoing-details.html'
    model = OutgoingLogModel
    pk_url_kwarg = 'pk'

    allowed_groups = ['admin', 'document_controller']

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        current_object = get_object_or_404(queryset, pk=pk)

        current_user_profile = self.request.user.profile
        current_user_groups = self.request.user.groups.values_list('name', flat=True)
        
        signatory_profile = current_object.signatory_profile
        

        rights = [
            set(current_user_groups).intersection(set(self.allowed_groups)),
            signatory_profile == current_user_profile,

            self.request.user.is_superuser,
            self.request.user.is_staff
        ]

        if not any(rights):
            raise Http404()
        
        return current_object

class OutgoingLogEditView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.UpdateView
):
    template_name = 'outgoing_log/outgoing-edit.html'
    form_class = EditOutgoingLogForm
    model = OutgoingLogModel

    allowed_groups = ['admin', 'document_controller']

    def get_object(self, queryset=None):
        # Get the object to edit based on the primary key (pk) from the URL
        pk = self.kwargs.get('pk')

        return get_object_or_404(self.model, pk=pk)
  
    def get_success_url(self):
        # Redirect to the details page of the edited object after successful update
        return reverse_lazy('outgoing-details', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        return super().form_valid(form)

class OutgoingLogDeleteView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.DeleteView
):
    template_name = 'outgoing_log/outgoing-delete.html'
    form_class = DeleteOutgoingLogForm
    model = OutgoingLogModel
    success_url = reverse_lazy('outgoing-dashboard')

    allowed_groups = ['admin',]

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')

        return get_object_or_404(self.model, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object

        if hasattr(self, 'form_class'):
            form_class = self.get_form_class()
            form = form_class(instance=instance)
            context['form'] = form

        return context
