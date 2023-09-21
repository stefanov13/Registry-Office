from django.contrib import admin
from .models import Profile, DepartmentsModel

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(DepartmentsModel)
class DepartmentsAdmin(admin.ModelAdmin):
    pass
