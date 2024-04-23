from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from django.http import HttpResponse
from itertools import chain
from core.mixins.moderator_group_mixin import GroupRequiredMixin
from core.custom_views.extra_content_views import ExtraContentListView
from ..news_feed.models import NewsFeedModel
from ..user_profiles.models import EmployeePositionsModel
from ..incoming_log.models import IncomingLogModel
from ..outgoing_log.models import OutgoingLogModel
from ..administrative_orders_log.models import AdministrativeOrdersLogModel
from ..contracts_log import models as contracts_models
from openpyxl import Workbook



class BaseNewsFeedView(views.ListView):
    template_name = 'common/index.html'
    model = NewsFeedModel

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        search = self.request.GET.get('search', '')

        queryset = self.model.objects.filter(
                title__icontains=search
            ).order_by('-date')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search'] = self.request.GET.get('search', '')
        context['rows_per_page'] = self.request.GET.get('rows_per_page', 8)

        return context
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('rows_per_page', 8)
    
class EmployeePositionsIdView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.ListView,
):
    template_name = 'common/employees-id-dashboard.html'
    model = EmployeePositionsModel
    
    allowed_groups = [
        'admin',
        'administrative_manager',
        'document_controller',
    ]
    
    def get_queryset(self):
        return self.model.objects.order_by('-pk')
    
class ContractTypesView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.ListView,
):
    template_name = 'common/contract-types-dashboard.html'
    model = contracts_models.ContractTypesModel
    
    allowed_groups = [
        'admin',
        'administrative_manager',
        'document_controller',
    ]
    
    def get_queryset(self):
        return self.model.objects.order_by('-pk')
    
class SearchAllRegistries(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.ListView,
):
    template_name = 'common/overall-search.html'

    allowed_groups = [
        'admin',
        'administrative_manager',
        'document_controller',
    ]

    all_models = (
        IncomingLogModel,
        OutgoingLogModel,
        AdministrativeOrdersLogModel,
        contracts_models.GeneralContractsLogModel,
        contracts_models.EducationContractsLogModel,
        contracts_models.FreelanceContractsLogModel,
        contracts_models.FreelanceLectureContractsLogModel,
    )

    def get_queryset(self, *args, **kwargs):
        self.search = self.request.GET.get('search', '')

        if self.search:
            search_result = [list(m.objects.filter(
                title__icontains=self.search
            )) for m in self.all_models]
            
            union_queryset = list(chain(*search_result))
            sorted_queryset = list(sorted(
                union_queryset,
                key=lambda x: x.creation_date.date(),
                reverse=True
            ))

            return sorted_queryset

        return list()
    
    def get(self, request, *args, **kwargs):
        if 'export' in request.GET:
            # If 'export' parameter is present in the query string, export data
            return self.export_data()
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        registries_names = {
            'IncomingLogModel': 'В',
            'OutgoingLogModel': 'И',
            'AdministrativeOrdersLogModel': 'З',
            'GeneralContractsLogModel': 'Д',
            'EducationContractsLogModel': 'ДО',
            'FreelanceContractsLogModel': 'ГД',
            'FreelanceLectureContractsLogModel': 'ГД-П'
        }

        context = super().get_context_data(**kwargs)

        context['reg_names'] = registries_names
        context['search'] = self.search
        context['rows_per_page'] = self.request.GET.get('rows_per_page', 8)

        return context
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('rows_per_page', 8)
    
    def export_data(self):
        # Retrieve the queryset
        queryset = self.get_queryset()

        # Create a new workbook and add a worksheet
        workbook = Workbook()
        worksheet = workbook.active

        # Write headers and data to the worksheet
        for obj in queryset:
            headers = []
            row = []

            for field in obj._meta.fields:
                headers.append(f'{field.verbose_name}') if field.is_relation else headers.append(str(field.verbose_name))
                row.append(str(getattr(obj, field.name))) if field.is_relation else row.append(str(getattr(obj, field.name)))

            worksheet.append(headers)
            worksheet.append(row)

        # Create a response with the Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=overall_search_results.xlsx'
        workbook.save(response)

        return response
    

class IncomingDashboardView(
    auth_mixins.LoginRequiredMixin,
    ExtraContentListView,
):
    template_name = 'common/incoming-dashboard.html'
    model = IncomingLogModel

class OutgoingDashboardView(
    auth_mixins.LoginRequiredMixin,
    ExtraContentListView,
):
    template_name = 'common/outgoing-dashboard.html'
    model = OutgoingLogModel
    
class OrdersDashboardView(
    auth_mixins.LoginRequiredMixin,
    ExtraContentListView,
):
    template_name = 'common/orders-dashboard.html'
    model = AdministrativeOrdersLogModel

class GeneralContractsDashboardView(
    auth_mixins.LoginRequiredMixin,
    ExtraContentListView,
):
    template_name = 'common/gen-contracts-dashboard.html'
    model = contracts_models.GeneralContractsLogModel

class EducationContractsDashboardView(
    auth_mixins.LoginRequiredMixin,
    ExtraContentListView,
):
    template_name = 'common/training-contracts-dashboard.html'
    model = contracts_models.EducationContractsLogModel

class FreelanceContractsDashboardView(
    auth_mixins.LoginRequiredMixin,
    ExtraContentListView,
):
    template_name = 'common/freelance-contracts-dashboard.html'
    model = contracts_models.FreelanceContractsLogModel

class FreelanceLectureContractsDashboardView(
    auth_mixins.LoginRequiredMixin,
    ExtraContentListView,
):
    template_name = 'common/freelance-lecturers-contracts-dashboard.html'
    model = contracts_models.FreelanceLectureContractsLogModel
