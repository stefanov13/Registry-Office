from django.contrib import admin
from .models import AdministrativeOrdersLogModel

# Register your models here.
@admin.register(AdministrativeOrdersLogModel)
class AdministrativeOrdersLogAdmin(admin.ModelAdmin):
    ordering = ('-pk',)
    list_display = ('log_num', 'title', 'creation_date', 'publisher',)
    list_filter = ('log_num', 'title', 'creation_date', 'publisher',)
    search_fields = ('log_num', 'title', 'creation_date', 'publisher',)
