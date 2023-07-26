from django.shortcuts import get_object_or_404, render
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .models import OutgoingLogModel
from .forms import CreateOutgoingLogForm, EditOutgoingLogForm, DeleteOutgoingLogForm

# Create your views here.


class OutgoingLogCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    NOT_SPECIFIED_CHOICE = _('Is Not Specified')
    template_name = 'outgoing_log/outgoing-create.html'
    form_class = CreateOutgoingLogForm
    success_url = reverse_lazy('outgoing-dashboard')

    def form_valid(self, form):
        # Get the cleaned data from the form
        cleaned_data = form.cleaned_data

        # Get the value of the custom_choice_field
        signatory_profile = cleaned_data.get('signatory_profile', )

        # Split the value by space (assuming it is formatted as "first_name last_name position")
        first_name, last_name, position = signatory_profile.split()
        if signatory_profile == self.NOT_SPECIFIED_CHOICE:
            first_name, last_name, position = self.NOT_SPECIFIED_CHOICE, '', self.NOT_SPECIFIED_CHOICE

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
    NOT_SPECIFIED_CHOICE = _('Is Not Specified')
    template_name = 'outgoing_log/outgoing-edit.html'
    form_class = EditOutgoingLogForm
    model = OutgoingLogModel

    def get_object(self, queryset=None):
        # Get the object to edit based on the primary key (pk) from the URL
        pk = self.kwargs.get('pk')
        return get_object_or_404(self.model, pk=pk)
  
    def get_success_url(self):
        # Redirect to the details page of the edited object after successful update
        return reverse_lazy('outgoing-details', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        signatory_profile = cleaned_data.get('signatory_profile', )

        first_name, last_name, position = signatory_profile.split()
        if signatory_profile == self.NOT_SPECIFIED_CHOICE:
            first_name, last_name, position = self.NOT_SPECIFIED_CHOICE, '', self.NOT_SPECIFIED_CHOICE

        form.instance.signatory_name = f'{first_name} {last_name}'
        form.instance.signatory_position = position

        return super().form_valid(form)

class OutgoingLogDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    template_name = 'outgoing_log/outgoing-delete.html'
    form_class = DeleteOutgoingLogForm
    model = OutgoingLogModel
    success_url = reverse_lazy('outgoing-dashboard')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(self.model, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object

        # Set the 'disabled' attribute for each field in the form
        if hasattr(self, 'form_class'):
            form_class = self.get_form_class()
            form = form_class(instance=instance)

            # for field_value in form.fields.values():
            #     field_value.widget.attrs['disabled'] = True

            context['form'] = form

        return context
