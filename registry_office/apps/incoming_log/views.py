from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy, reverse
from django.contrib.auth import mixins as auth_mixins
from django.views import generic as views
from core.mixins.moderator_group_mixin import GroupRequiredMixin
from core.custom_views.extra_content_views import ExtraContentCreateView
from core.doc_files_context import extra_context_details_view
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
        'concerned_employees',
        'first_document_file',
        'second_document_file',
        'third_document_file'
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
                concerned_employees__in=self.current_user_ids
                ).order_by('-pk')

        return queryset
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        current_object = get_object_or_404(queryset, pk=pk)

        responsible_employees = current_object.concerned_employees.all()

        current_user_auth = True if set(responsible_employees).intersection(self.current_user_ids) else False
        context['is_auth'] = current_user_auth

        context['doc_files'] = extra_context_details_view(current_object)

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
        if self.rights:
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
                set(self.get_object().concerned_employees.all())
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
        response = super().form_valid(form)

        opinion = form.cleaned_data.get('opinion', None)
        # log_num = form.cleaned_data.get('log_num', None)
        # current_creation_date = form.cleaned_data.get('creation_date')

        # log_num_range_in_date = IncomingLogModel.objects.filter(
        #     creation_date__date=self.object.creation_date.date()
        # ).all()

        # range_log_nums = [x.log_num for x in log_num_range_in_date]

        # last_log_num_before_date = IncomingLogModel.objects.filter(
        #     creation_date__year=self.object.creation_date.year,
        #     creation_date__lte=self.object.creation_date.date()
        # ).order_by(
        #     '-log_num'
        # ).first()
        
        if self.object.personopinionmodel_set.filter(
            profile_owner_id=self.request.user.profile.pk
            ).exists():
            po = PersonOpinionModel.objects.filter(
                profile_owner=self.request.user.profile,
                document=self.object
            ).get()
            
            po.opinion = opinion
            po.save()

        elif opinion:
            po = PersonOpinionModel.objects.create(
                profile_owner=self.request.user.profile,
                opinion=opinion, 
                document=self.object
            )
            
            po.save()
            form.instance.opinions = po

        # constraints = (log_num_range_in_date, last_log_num_before_date.log_num == self.object.log_num)

        # if not any(constraints):
        #     raise ValidationError(
        #         _('Номерът, който се оптвате да въведете или не е от тази дата или не е последния номер от предходната дата от тази на регистрацията')
        #     ) # Номерът, който се оптвате да въведете или не е от тази дата или не е последния номер от предходната дата от тази на регистрацията

        return response
    
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
