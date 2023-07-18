from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import generic as views
from django.contrib.auth import login, views as auth_views, mixins as auth_mixins, get_user_model
from .forms import RegisterUserForm

# Create your views here.

UserModel = get_user_model()

class RegisterUserView(views.CreateView):
    template_name = 'accounts/signup.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        current_object = self.object
        
        login(self.request, current_object)
        
        return result


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'

class UserLogoutView(auth_views.LogoutView):
    pass

class UserDetailsView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = UserModel
    template_name = 'accounts/user-details.html'
