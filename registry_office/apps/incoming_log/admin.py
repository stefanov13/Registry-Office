from django.contrib import admin
from .models import IncomingLogModel

# Register your models here.
@admin.register(IncomingLogModel)
class IncomingLogAdmin(admin.ModelAdmin):
    ordering = ('-pk',)
    list_display = (
        'log_num',
        'sub_log_num',
        'title',
        'creation_date',
        'rectors_resolution',
        'creator_user',
        'last_change_date',
    )
    list_filter = (
        'log_num',
        'sub_log_num',
        'title',
        'creation_date',
        'rectors_resolution',
        'creator_user',
        'last_change_date',
    )
    search_fields = (
        'log_num',
        'sub_log_num',
        'title',
        'creation_date',
        'rectors_resolution',
        'creator_user',
        'last_change_date',
    )
    