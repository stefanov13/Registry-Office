from django.forms.models import BaseModelForm
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import mixins as auth_mixins
from django.views import generic as views
from core.mixins.moderator_group_mixin import GroupRequiredMixin
from .models import IncomingLogModel, PersonOpinion
from .forms import EditIncomingLogForm

# Create your views here.

class IncomingLogCreateView(GroupRequiredMixin, views.CreateView):
    template_name = 'incoming_log/incoming-create.html'
    success_url = reverse_lazy('incoming-dashboard')
    model = IncomingLogModel
    fields = ['category', 'title', 'responsible_persons', 'document_img']

    allowed_groups = ['admin', 'document_controller']

class IncomingLogDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    template_name = 'incoming_log/incoming-details.html'
    model = IncomingLogModel

    allowed_groups = ['admin', 'document_controller']

    def get_queryset(self):
        current_user_profile = self.request.user.profile
        current_user_groups = self.request.user.groups.values_list('name', flat=True)
        if any([set(current_user_groups).intersection(set(self.allowed_groups)), self.request.user.is_superuser, self.request.user.is_staff]):
            queryset = self.model.objects.order_by('-pk')
        else:
            queryset = self.model.objects.filter(responsible_persons__in=[current_user_profile]).order_by('-pk')

        return queryset

class IncomingLogEditView(auth_mixins.LoginRequiredMixin, auth_mixins.UserPassesTestMixin, views.UpdateView):
    template_name = 'incoming_log/incoming-edit.html'
    form_class = EditIncomingLogForm
    model = IncomingLogModel

    allowed_groups = ['admin', 'document_controller']

    def test_func(self):
        current_user_groups = self.request.user.groups.values_list('name', flat=True)

        return any([set(current_user_groups).intersection(set(self.allowed_groups)), self.request.user.is_superuser, self.request.user.is_staff]) or self.request.user.profile in self.get_object().responsible_persons.all()
    
    def handle_no_permission(self):
        raise Http404()
    
    def form_valid(self, form):
        opinion = form.cleaned_data.get('opinion', None)

        if self.object.personopinion_set.filter(profile_owner_id=self.request.user.profile.pk).exists():
            po = PersonOpinion.objects.filter(profile_owner = self.request.user.profile).get()
            po.opinion = opinion
            po.save()
        elif opinion:
            po = PersonOpinion.objects.create(profile_owner = self.request.user.profile, opinion=opinion, document=self.object)
            po.save()
            form.instance.opinions = po

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('incoming-details', kwargs={'pk': self.kwargs['pk']})
         
class IncomingLogDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    pass
