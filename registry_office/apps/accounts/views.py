from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views import generic as views
from django.contrib.auth import login, views as auth_views, mixins as auth_mixins, get_user_model
from django.http import Http404
from .forms import RegisterUserForm, EditUserForm

# Create your views here.

UserModel = get_user_model()

class UserRegisterView(auth_mixins.UserPassesTestMixin, views.CreateView):
    template_name = 'accounts/signup.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        current_object = self.object
        
        login(self.request, current_object)
        
        return result


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

class UserLogoutView(auth_views.LogoutView):
    pass

class UserDetailsView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = UserModel
    template_name = 'accounts/user-details.html'

class UserEditView(auth_mixins.UserPassesTestMixin,
                   auth_mixins.LoginRequiredMixin,
                   views.UpdateView):
    model = UserModel
    template_name = 'accounts/user-edit.html'
    form_class = EditUserForm

    def test_func(self):
        return self.get_object().pk == self.request.user.pk or self.request.user.is_superuser \
            or self.request.user.is_staff
    
    def handle_no_permission(self):
        raise Http404()
    
    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('user-details') 

class UserDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    template_name = 'accounts/user-delete.html'
    success_url = reverse_lazy('index')
    
    def get_object(self, queryset=None):
        return self.request.user

class UserChangePasswordView(auth_mixins.LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('user-details')

