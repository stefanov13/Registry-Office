from django.shortcuts import render
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy
from .forms import CreateOutgoingLogForm, EditOutgoingLogForm, DeleteOutgoingLogForm

# Create your views here.


class OutgoingLogCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    template_name = 'outgoing_log/outgoing-create.html'
    form_class = CreateOutgoingLogForm
    success_url = reverse_lazy('outgoing-dashboard')

class OutgoingLogDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    template_name = 'outgoing_log/outgoing-details.html'

class OutgoingLogEditView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    template_name = 'outgoing_log/outgoing-edit.html'
    form_class = EditOutgoingLogForm
    success_url = reverse_lazy('outgoing-details') 

class OutgoingLogDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    template_name = 'outgoing_log/outgoing-delete.html'
    form_class = DeleteOutgoingLogForm
    success_url = reverse_lazy('outgoing-dashboard')
