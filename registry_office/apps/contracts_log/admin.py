from django.contrib import admin
from . import models


@admin.register(models.ContractTypesModel)
class ContractTypesAdmin(admin.ModelAdmin):
    ordering = ('-pk',)
    list_display = ('contract_type',)
    list_filter = ('contract_type',)
    search_fields = ('contract_type',)

@admin.register(models.GeneralContractsLogModel)
class GeneralContractsLogAdmin(admin.ModelAdmin):
    ordering = ('-pk',)
    list_display = (
        'log_num',
        'sub_log_num',
        'creation_date',
        'title',
        'contract_type',
        'creator_user',
    )

    list_filter = (
        'log_num',
        'sub_log_num',
        'creation_date',
        'title',
        'contract_type',
        'creator_user',
    )

    search_fields = (
        'log_num',
        'sub_log_num',
        'creation_date',
        'title',
        'contract_type',
        'creator_user',
    )

@admin.register(models.EducationContractsLogModel)
class EducationContractsLogAdmin(admin.ModelAdmin):
    ordering = ('-pk',)
    list_display = (
        'log_num',
        'sub_log_num',
        'creation_date',
        'title',
        'contract_type',
        'creator_user',
    )

    list_filter = (
        'log_num',
        'sub_log_num',
        'creation_date',
        'title',
        'contract_type',
        'creator_user',
    )

    search_fields = (
        'log_num',
        'sub_log_num',
        'creation_date',
        'title',
        'contract_type',
        'creator_user',
    )

@admin.register(models.FreelanceContractsLogModel)
class FreelanceContractsLogAdmin(admin.ModelAdmin):
    ordering = ('-pk',)
    list_display = (
        'log_num',
        'sub_log_num',
        'creation_date',
        'title',
        'contract_type',
        'creator_user',
    )

    list_filter = (
        'log_num',
        'sub_log_num',
        'creation_date',
        'title',
        'contract_type',
        'creator_user',
    )

    search_fields = (
        'log_num',
        'sub_log_num',
        'creation_date',
        'title',
        'contract_type',
        'creator_user',
    )

@admin.register(models.FreelanceLectureContractsLogModel)
class FreelanceLectureContractsLogAdmin(admin.ModelAdmin):
    ordering = ('-pk',)
    list_display = (
        'log_num',
        'sub_log_num',
        'creation_date',
        'title',
        'contract_type',
        'creator_user',
    )

    list_filter = (
        'log_num',
        'sub_log_num',
        'creation_date',
        'title',
        'contract_type',
        'creator_user',
    )

    search_fields = (
        'log_num',
        'sub_log_num',
        'creation_date',
        'title',
        'contract_type',
        'creator_user',
    )
