from django.shortcuts import get_object_or_404, render
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .models import OutgoingLogModel
from .forms import CreateOutgoingLogForm, EditOutgoingLogForm, DeleteOutgoingLogForm

# Create your views here.


class OutgoingLogCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    template_name = 'outgoing_log/outgoing-create.html'
    form_class = CreateOutgoingLogForm
    success_url = reverse_lazy('outgoing-dashboard')

    def form_valid(self, form):
        # Get the cleaned data from the form
        cleaned_data = form.cleaned_data

        # Get the value of the custom_choice_field
        custom_choice_value = cleaned_data.get('custom_choice_field', )

        # Split the value by space (assuming it is formatted as "first_name last_name position")
        try:
            first_name, last_name, position = custom_choice_value.split()
        except ValueError:
            first_name, last_name, position = _('Not'), _('Present'), _('Not Present')

        # Assign the split values to the corresponding fields
        form.instance.signatory_name = f'{first_name} {last_name}'
        form.instance.signatory_position = position

        # Call the parent's form_valid method to save the form and return the response
        return super().form_valid(form)

class OutgoingLogDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    template_name = 'outgoing_log/outgoing-details.html'
    model = OutgoingLogModel
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        # Override get_object to fetch the object based on the pk_url_kwarg
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(queryset, pk=pk)


class OutgoingLogEditView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    template_name = 'outgoing_log/outgoing-edit.html'
    form_class = EditOutgoingLogForm
    success_url = reverse_lazy('outgoing-details') 

class OutgoingLogDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    template_name = 'outgoing_log/outgoing-delete.html'
    form_class = DeleteOutgoingLogForm
    success_url = reverse_lazy('outgoing-dashboard')