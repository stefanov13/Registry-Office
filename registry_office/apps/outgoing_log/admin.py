from django.contrib import admin
from .models import OutgoingLogModel

# Register your models here.

@admin.register(OutgoingLogModel)
class OutgoingLogAdmin(admin.ModelAdmin):
    ordering = ('-log_num',)
    list_display = (
        'log_num',
        'sub_log_num',
        'title',
        'recipient',
        'creation_date',
        'creator_user',
    )

    list_filter = (
        'log_num',
        'sub_log_num',
        'title',
        'recipient',
        'creation_date',
        'creator_user',
    )
    
    search_fields = (
        'log_num',
        'sub_log_num',
        'title',
        'recipient',
        'creation_date',
        'creator_user',
    )
