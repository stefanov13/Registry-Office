from django.contrib import admin
from .models import Profile, EmployeePositionsModel

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(EmployeePositionsModel)
class EmployeePositionsAdmin(admin.ModelAdmin):
    pass
