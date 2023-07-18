from django.contrib import admin
from .models import AppCustomUser

# Register your models here.
@admin.register(AppCustomUser)
class AppCustomUserAdmin(admin.ModelAdmin):
    pass