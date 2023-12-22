from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import mixins as auth_mixins
from django.views import generic as views
from core.mixins.moderator_group_mixin import GroupRequiredMixin
from .models import EmployeePositionsModel
from .forms import EditEmployeePositionsForm, DeleteEmployeePositionsForm

class EmployeePositionsCreateView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.CreateView
):
    template_name = 'user_profiles/employee-position-create.html'
    success_url = reverse_lazy('positions-id-dashboard')
    model = EmployeePositionsModel
    fields = '__all__'

    allowed_groups = [
        'admin',
        'administrative_manager',
        'document_controller',
    ]

class EmployeePositionsDetailsView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.DetailView
):
    template_name = 'user_profiles/employee-position-details.html'
    model = EmployeePositionsModel

    allowed_groups = [
        'admin', 
        'administrative_manager', 
        'document_controller',
    ]

class EmployeePositionsEditView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.UpdateView
):
    template_name = 'user_profiles/employee-position-edit.html'
    form_class = EditEmployeePositionsForm
    model = EmployeePositionsModel

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
        return reverse_lazy('employee-pos-details', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        return super().form_valid(form)

class EmployeePositionsDeleteView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.DeleteView
):
    template_name = 'user_profiles/employee-position-delete.html'
    form_class = DeleteEmployeePositionsForm
    model = EmployeePositionsModel
    success_url = reverse_lazy('positions-id-dashboard')

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
