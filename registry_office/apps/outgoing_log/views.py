from django.shortcuts import render
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy
from .forms import CreateOutgoingLogForm

# Create your views here.


class OutgoingLogCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    template_name = 'accounts/signup.html'
    form_class = CreateOutgoingLogForm
    success_url = reverse_lazy('index')
