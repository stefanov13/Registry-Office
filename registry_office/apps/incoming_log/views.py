from typing import Any
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import mixins as auth_mixins
from django.views import generic as views
from core.mixins.moderator_group_mixin import GroupRequiredMixin
from core.custom_views.extra_content_create_view import ExtraContentCreateView
from .models import IncomingLogModel, PersonOpinionModel
from . import forms


class IncomingLogCreateView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    ExtraContentCreateView
):
    template_name = 'incoming_log/incoming-create.html'
    success_url = reverse_lazy('incoming-dashboard')
    model = IncomingLogModel
    fields = [
        'title',
        'responsible_employees',
        'document_file'
    ]

    allowed_groups = [
        'admin',
        'administrative_manager',
        'document_controller',
    ]

class IncomingLogDetailsView(
    auth_mixins.LoginRequiredMixin,
    views.DetailView
):
    template_name = 'incoming_log/incoming-details.html'
    model = IncomingLogModel
    pk_url_kwarg = 'pk'

    allowed_groups = [
        'admin', 
        'administrative_manager', 
        'document_controller',
    ]

    # def dispatch(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     pk = self.kwargs.get(self.pk_url_kwarg)
    #     current_object = get_object_or_404(queryset, pk=pk)

    #     current_user_ids = self.request.user.profile.employeepositionsmodel_set.all()
    #     current_user_groups = request.user.groups.values_list('name', flat=True)

    #     responsible_employees = current_object.responsible_employees.all()

    #     rights = [
    #         set(current_user_groups).intersection(set(self.allowed_groups)),
    #         set(current_user_ids).intersection(set(responsible_employees)),
    #         self.request.user.is_superuser,
    #         self.request.user.is_staff,
    #     ]
        
    #     if not any(rights):
    #         return self.handle_no_permission()

    #     return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.current_user_ids = self.request.user.profile.employeepositionsmodel_set.all()
        current_user_groups = self.request.user.groups.values_list('name', flat=True)

        rights = [
            set(current_user_groups).intersection(set(self.allowed_groups)),
            self.request.user.is_superuser,
            self.request.user.is_staff
        ]

        if any(rights):
            queryset = self.model.objects.order_by('-pk') 

        else:
            queryset = self.model.objects.filter(
                responsible_employees__in=self.current_user_ids
                ).order_by('-pk')

        return queryset
    
    def get_context_data(self, *args, **kwargs: Any):
        context = super().get_context_data(*args, **kwargs)

        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        current_object = get_object_or_404(queryset, pk=pk)

        responsible_employees = current_object.responsible_employees.all()

        current_user_auth = True if set(responsible_employees).intersection(self.current_user_ids) else False
        context['is_auth'] = current_user_auth

        return context

class IncomingLogEditView(
    auth_mixins.LoginRequiredMixin,
    auth_mixins.UserPassesTestMixin,
    views.UpdateView
):
    template_name = 'incoming_log/incoming-edit.html'
    model = IncomingLogModel

    allowed_groups = ['admin', 'administrative_manager']
    document_controller_group = 'document_controller'

    def get_form_class(self):
        if any(self.rights):
            return forms.EditIncomingLogForm
        
        elif self.document_controller_group in self.current_user_groups:
            return forms.EditIncomingLogDocControllerForm
        
        # elif self.request.user.profile in self.get_object().responsible_people.all():
        return forms.EditIncomingLogOpinionForm

    def test_func(self):
        self.current_user_groups = self.request.user.groups.values_list('name', flat=True)

        self.rights = [
            set(self.current_user_groups).intersection(set(self.allowed_groups)),
            self.request.user.is_superuser,
            self.request.user.is_staff,
        ]

        return any(self.rights) \
            or self.document_controller_group in self.current_user_groups \
            or set(
                self.request.user.profile.employeepositionsmodel_set.all()
            ).intersection(
                set(self.get_object().responsible_employees.all())
            )
    
    def handle_no_permission(self):
        raise Http404()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object

        return context
    
    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user

        try:
            person_opinion = PersonOpinionModel.objects.filter(
                profile_owner=user.profile,
                document=self.object
            ).get()
            
            initial['opinion'] = person_opinion.opinion
            
        except PersonOpinionModel.DoesNotExist:
            pass

        return initial
    
    def form_valid(self, form):
        opinion = form.cleaned_data.get('opinion', None)
        
        if self.object.personopinionmodel_set.filter(
            profile_owner_id=self.request.user.profile.pk
            ).exists():
            po = PersonOpinionModel.objects.filter(
                profile_owner=self.request.user.profile,
                document=self.object).get()
            
            po.opinion = opinion
            po.save()

        elif opinion:
            po = PersonOpinionModel.objects.create(
                profile_owner=self.request.user.profile,
                opinion=opinion, document=self.object)
            
            po.save()
            form.instance.opinions = po

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('incoming-details', kwargs={'pk': self.object.pk})
         
class IncomingLogDeleteView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.DeleteView
):
    template_name = 'incoming_log/incoming-delete.html'
    form_class = forms.DeleteIncomingLogForm
    model = IncomingLogModel
    success_url = reverse_lazy('incoming-dashboard')

    allowed_groups = ['admin']

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

class PersonOpinionEditView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.UpdateView
):
    template_name = 'incoming_log/person-opinion-edit.html'
    model = PersonOpinionModel
    form_class = forms.EditPersonOpinionForm
    allowed_groups = ['admin']

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')

        return get_object_or_404(self.model, pk=pk)
    
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('incoming-details', kwargs={'pk': self.object.document_id})

class PersonOpinionDeleteView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.DeleteView
):
    template_name = 'incoming_log/person-opinion-delete.html'
    form_class = forms.DeletePersonOpinionForm
    model = PersonOpinionModel

    allowed_groups = ['admin']

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

    def get_success_url(self):
        return reverse('incoming-details', kwargs={'pk': self.object.document_id})
