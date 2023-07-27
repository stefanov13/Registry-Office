from django.contrib import admin
from .models import IncomingLogModel

# Register your models here.
@admin.register(IncomingLogModel)
class IncomingLogAdmin(admin.ModelAdmin):
    pass
