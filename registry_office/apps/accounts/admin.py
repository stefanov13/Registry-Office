from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import AppCustomUser
from .forms import RegisterUserForm

# Register your models here.
@admin.register(AppCustomUser)
class AppCustomUserAdmin(auth_admin.UserAdmin):
    add_form = RegisterUserForm
    ordering = ('email',)
    list_display = ('email',)
    fieldsets = (
        (_('Credentials'), {'fields': ('email', 'password')}),
    )
