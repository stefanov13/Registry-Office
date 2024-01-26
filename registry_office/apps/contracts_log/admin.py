from django.contrib import admin
from .models import ContractTypesModel, GeneralContractsLogModel, EducationContractsLogModel

# Register your models here.
@admin.register(ContractTypesModel)
class ContractTypesAdmin(admin.ModelAdmin):
    ordering = ('-pk',)
    list_display = ('contract_type',)
    list_filter = ('contract_type',)
    search_fields = ('contract_type',)

@admin.register(GeneralContractsLogModel)
class GeneralContractsLogAdmin(admin.ModelAdmin):
    ordering = ('-pk',)
    list_display = ('log_num', 'creation_date', 'title',)
    list_filter = ('log_num', 'creation_date', 'title',)
    search_fields = ('log_num', 'creation_date', 'title',)

@admin.register(EducationContractsLogModel)
class EducationContractsLogAdmin(admin.ModelAdmin):
    ordering = ('-pk',)
    list_display = ('log_num', 'creation_date', 'title',)
    list_filter = ('log_num', 'creation_date', 'title',)
    search_fields = ('log_num', 'creation_date', 'title',)
