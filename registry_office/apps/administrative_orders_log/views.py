from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import mixins as auth_mixins
from django.views import generic as views
from core.mixins.moderator_group_mixin import GroupRequiredMixin
from core.custom_views.extra_content_views import ExtraContentCreateView
from .models import AdministrativeOrdersLogModel
from . import forms


class AdministrativeOrdersLogCreateView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    ExtraContentCreateView,
):
    template_name = 'administrative_orders_log/orders-create.html'
    success_url = reverse_lazy('orders-dashboard')
    model = AdministrativeOrdersLogModel
    fields = [
        'title',
        'publisher',
        'responsible_employees',
        'document_file',
    ]

    allowed_groups = [
        'admin',
        'administrative_manager',
        'document_controller',
    ]

class AdministrativeOrdersLogDetailsView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.DetailView,
):
    template_name = 'administrative_orders_log/orders-details.html'
    model = AdministrativeOrdersLogModel
    pk_url_kwarg = 'pk'

    allowed_groups = [
        'admin', 
        'administrative_manager', 
        'document_controller',
    ]

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)

        return get_object_or_404(queryset, pk=pk)

class AdministrativeOrdersLogEditView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.UpdateView,
):
    template_name = 'administrative_orders_log/orders-edit.html'
    model = AdministrativeOrdersLogModel
    fields = '__all__'

    allowed_groups = [
        'admin', 
        'administrative_manager', 
        'document_controller',
    ]

    def get_object(self, queryset=None):
        # Get the object to edit based on the primary key (pk) from the URL
        pk = self.kwargs.get('pk')

        return get_object_or_404(self.model, pk=pk)

    def get_success_url(self):
        # Redirect to the details page of the edited object after successful update
        return reverse_lazy('orders-details', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        return super().form_valid(form)
    
class AdministrativeOrdersLogDeleteView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.DeleteView,
):
    template_name = 'administrative_orders_log/orders-delete.html'
    form_class = forms.DeleteAdministrativeOrdersLogForm
    model = AdministrativeOrdersLogModel
    success_url = reverse_lazy('orders-dashboard')

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
