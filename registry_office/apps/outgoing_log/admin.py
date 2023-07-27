from django.contrib import admin
from .models import OutgoingLogModel

# Register your models here.

@admin.register(OutgoingLogModel)
class OutgoingLogAdmin(admin.ModelAdmin):
    pass
