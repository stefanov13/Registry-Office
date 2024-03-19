from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import mixins as auth_mixins
from django.views import generic as views
from core.mixins.moderator_group_mixin import GroupRequiredMixin
from core.custom_views.extra_content_views import ExtraContentCreateView
from core.doc_files_context import extra_context_details_view
from . import models
from . import forms


class ContractTypesCreateView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.CreateView,
):
    template_name = 'contracts_log/contract-types-create.html'
    model = models.ContractTypesModel
    fields = '__all__'
    success_url = reverse_lazy('contract-types-dashboard')

    allowed_groups = [
        'admin',
        'administrative_manager',
        'document_controller',
    ]

class ContractTypesEditView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.UpdateView,
):
    template_name = 'contracts_log/contract-types-edit.html'
    model = models.ContractTypesModel
    fields = '__all__'
    success_url = reverse_lazy('contract-types-dashboard')

    allowed_groups = [
        'admin', 
        'administrative_manager', 
        'document_controller',
    ]

    def get_object(self, queryset=None):
        # Get the object to edit based on the primary key (pk) from the URL
        pk = self.kwargs.get('pk')

        return get_object_or_404(self.model, pk=pk)
    
    def form_valid(self, form):
        return super().form_valid(form)
    
class ContractTypesDeleteView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.DeleteView,
):
    template_name = 'contracts_log/contract-types-delete.html'
    model = models.ContractTypesModel
    form_class = forms.DeleteContractTypesForm
    success_url = reverse_lazy('contract-types-dashboard')
    
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

class ContractsLogCreateView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    ExtraContentCreateView,
):
    fields = [
        'title',
        'contract_type',
        'concerned_employees',
        'first_document_file',
        'second_document_file',
        'third_document_file',
    ]

    allowed_groups = [
        'admin',
        'administrative_manager',
        'document_controller',
    ]

class ContractsLogDetailsView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.DetailView,
):
    pk_url_kwarg = 'pk'

    allowed_groups = [
        'admin', 
        'administrative_manager', 
        'document_controller',
    ]

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        self.current_object = get_object_or_404(queryset, pk=pk)

        return self.current_object
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['doc_files'] = extra_context_details_view(self.current_object)

        return context

class ContractsLogEditView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.UpdateView,
):
    exclude = ['creator_user']

    allowed_groups = [
        'admin', 
        'administrative_manager', 
        'document_controller',
    ]

    def get_object(self, queryset=None):
        # Get the object to edit based on the primary key (pk) from the URL
        pk = self.kwargs.get('pk')

        return get_object_or_404(self.model, pk=pk)
    
    def form_valid(self, form):
        return super().form_valid(form)
    
class ContractsLogDeleteView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.DeleteView,
):
    form_class = forms.DeleteContractsLogForm
    
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

class GeneralContractsLogCreateView(ContractsLogCreateView):
    template_name = 'contracts_log/gen-contracts-create.html'
    model = models.GeneralContractsLogModel
    success_url = reverse_lazy('gen-contracts-dashboard')

class GeneralContractsLogDetailsView(ContractsLogDetailsView):
    template_name = 'contracts_log/gen-contracts-details.html'
    model = models.GeneralContractsLogModel

class GeneralContractsLogEditView(ContractsLogEditView):
    template_name = 'contracts_log/gen-contracts-edit.html'
    model = models.GeneralContractsLogModel

    def get_success_url(self):
        # Redirect to the details page of the edited object after successful update
        return reverse_lazy('gen-contracts-details', kwargs={'pk': self.object.pk})

class GeneralContractsLogDeleteView(ContractsLogDeleteView):
    template_name = 'contracts_log/gen-contracts-delete.html'
    model = models.GeneralContractsLogModel
    success_url = reverse_lazy('gen-contracts-dashboard')

class EducationContractsLogCreateView(ContractsLogCreateView):
    template_name = 'contracts_log/training-contracts-create.html'
    model = models.EducationContractsLogModel
    success_url = reverse_lazy('training-contracts-dashboard')

class EducationContractsLogDetailsView(ContractsLogDetailsView):
    template_name = 'contracts_log/training-contracts-details.html'
    model = models.EducationContractsLogModel

class EducationContractsLogEditView(ContractsLogEditView):
    template_name = 'contracts_log/training-contracts-edit.html'
    model = models.EducationContractsLogModel

    def get_success_url(self):
        # Redirect to the details page of the edited object after successful update
        return reverse_lazy('training-contracts-details', kwargs={'pk': self.object.pk})
    
class EducationContractsLogDeleteView(ContractsLogDeleteView):
    template_name = 'contracts_log/training-contracts-delete.html'
    model = models.EducationContractsLogModel
    success_url = reverse_lazy('training-contracts-dashboard')

class FreelanceContractsLogCreateView(ContractsLogCreateView):
    template_name = 'contracts_log/freelance-contracts-create.html'
    model = models.FreelanceContractsLogModel
    success_url = reverse_lazy('freelance-contracts-dashboard')

class FreelanceContractsLogDetailsView(ContractsLogDetailsView):
    template_name = 'contracts_log/freelance-contracts-details.html'
    model = models.FreelanceContractsLogModel

class FreelanceContractsLogEditView(ContractsLogEditView):
    template_name = 'contracts_log/freelance-contracts-edit.html'
    model = models.FreelanceContractsLogModel

    def get_success_url(self):
        # Redirect to the details page of the edited object after successful update
        return reverse_lazy('freelance-contracts-details', kwargs={'pk': self.object.pk})
    
class FreelanceContractsLogDeleteView(ContractsLogDeleteView):
    template_name = 'contracts_log/freelance-contracts-delete.html'
    model = models.FreelanceContractsLogModel
    success_url = reverse_lazy('freelance-contracts-dashboard')

class FreelanceLectureContractsLogCreateView(ContractsLogCreateView):
    template_name = 'contracts_log/freelance-lecturers-contracts-create.html'
    model = models.FreelanceLectureContractsLogModel
    success_url = reverse_lazy('freelance-lecturers-contracts-dashboard')

class FreelanceLectureContractsLogDetailsView(ContractsLogDetailsView):
    template_name = 'contracts_log/freelance-lecturers-contracts-details.html'
    model = models.FreelanceLectureContractsLogModel

class FreelanceLectureContractsLogEditView(ContractsLogEditView):
    template_name = 'contracts_log/freelance-lecturers-contracts-edit.html'
    model = models.FreelanceLectureContractsLogModel

    def get_success_url(self):
        # Redirect to the details page of the edited object after successful update
        return reverse_lazy('freelance-lecturers-contracts-details', kwargs={'pk': self.object.pk})
    
class FreelanceLectureContractsLogDeleteView(ContractsLogDeleteView):
    template_name = 'contracts_log/freelance-lecturers-contracts-delete.html'
    model = models.FreelanceLectureContractsLogModel
    success_url = reverse_lazy('freelance-lecturers-contracts-dashboard')
