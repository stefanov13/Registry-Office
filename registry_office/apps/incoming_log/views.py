from django.shortcuts import render
from django.contrib.auth import mixins as auth_mixins
from django.views import generic as views

# Create your views here.

class IncomingLogCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    pass

class IncomingLogDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    pass

class IncomingLogEditView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    pass

class IncomingLogDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    pass
