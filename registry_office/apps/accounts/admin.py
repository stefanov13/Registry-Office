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
    list_display = ('email', 'is_staff', 'is_active', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    fieldsets = (
        (_('Credentials'), {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            _('Create User'),
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'position'),
            },
        ),
    )
