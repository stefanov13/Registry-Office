from django.contrib import admin
from .models import AdministrativeOrdersLogModel

# Register your models here.
@admin.register(AdministrativeOrdersLogModel)
class AdministrativeOrdersLogAdmin(admin.ModelAdmin):
    ordering = ('-pk',)
    list_display = (
        'log_num',
        'sub_log_num',
        'title',
        'creation_date',
        'publisher',
        'creator_user',
    )

    list_filter = (
        'log_num',
        'sub_log_num',
        'title',
        'creation_date',
        'publisher',
        'creator_user',
    )

    search_fields = (
        'log_num',
        'sub_log_num',
        'title',
        'creation_date',
        'publisher',
        'creator_user',
    )
