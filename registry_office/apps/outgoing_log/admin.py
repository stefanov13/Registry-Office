from django.contrib import admin
from .models import OutgoingLogModel

# Register your models here.

@admin.register(OutgoingLogModel)
class OutgoingLogAdmin(admin.ModelAdmin):
    ordering = ('-log_num',)
    list_display = ('log_num', 'title', 'recipient', 'creation_date',)
    list_filter = ('log_num', 'title', 'recipient', 'creation_date',)
    search_fields = ('log_num', 'title', 'recipient', 'creation_date',)
