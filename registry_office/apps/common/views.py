from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from django.utils.dateparse import parse_date
from itertools import chain
from core.mixins.moderator_group_mixin import GroupRequiredMixin
from core.custom_views import extra_content_views
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

    DEFAULT_FROM_DATE = '2023-01-01'

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

    registries_names = {
            'IncomingLogModel': 'В',
            'OutgoingLogModel': 'И',
            'AdministrativeOrdersLogModel': 'З',
            'GeneralContractsLogModel': 'Д',
            'EducationContractsLogModel': 'ДО',
            'FreelanceContractsLogModel': 'ГД',
            'FreelanceLectureContractsLogModel': 'ГД-П'
        }

    def get_queryset(self, *args, **kwargs):
        self.current_date = timezone.now().date().strftime('%Y-%m-%d')

        self.search = self.request.GET.get('search', '')
        words = self.search.strip().split()

        # Build a Q object for each word
        query = Q()
        for word in words:
            query &= Q(title__icontains=word)

        self.from_date = self.request.GET.get('from-date', self.DEFAULT_FROM_DATE)
        self.to_date = self.request.GET.get('to-date', self.current_date)

        self.from_date = parse_date(self.from_date)
        self.to_date = parse_date(self.to_date)

        if not self.from_date:
            self.from_date = self.DEFAULT_FROM_DATE

        if not self.to_date:
            self.to_date = self.current_date

        if self.search:
            search_result = [list(m.objects.filter(
                query,
                creation_date__date__gte=self.from_date,
                creation_date__date__lte=self.to_date
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
        context = super().get_context_data(**kwargs)

        context['reg_names'] = self.registries_names
        context['search'] = self.search
        context['from_date'] = self.from_date.strftime('%Y-%m-%d') if not isinstance(self.from_date, str) else self.from_date
        context['to_date'] = self.to_date.strftime('%Y-%m-%d') if not isinstance(self.to_date, str) else self.to_date
        context['current_date'] = self.current_date
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
            # headers = []
            row = []

            row.append(self.registries_names.get(obj.__class__.__name__, ''))

            for field in obj._meta.fields:
                # headers.append(f'{field.verbose_name}') if field.is_relation else headers.append(str(field.verbose_name))
                row.append(str(getattr(obj, field.name))) if field.is_relation else row.append(str(getattr(obj, field.name)))

            # worksheet.append(headers)
            worksheet.append(row)

        # Create a response with the Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=overall_search_results.xlsx'
        workbook.save(response)

        return response
    
class IncomingDashboardView(
    auth_mixins.LoginRequiredMixin,
    extra_content_views.ExtraContentListView,
):
    template_name = 'common/incoming-dashboard.html'
    model = IncomingLogModel

class OutgoingDashboardView(
    auth_mixins.LoginRequiredMixin,
    extra_content_views.ExtraContentListView,
):
    template_name = 'common/outgoing-dashboard.html'
    model = OutgoingLogModel
    
class OrdersDashboardView(
    auth_mixins.LoginRequiredMixin,
    extra_content_views.ExtraContentListView,
):
    template_name = 'common/orders-dashboard.html'
    model = AdministrativeOrdersLogModel

class GeneralContractsDashboardView(
    auth_mixins.LoginRequiredMixin,
    extra_content_views.ExtraContentContractListView,
):
    template_name = 'common/gen-contracts-dashboard.html'
    model = contracts_models.GeneralContractsLogModel

class EducationContractsDashboardView(
    auth_mixins.LoginRequiredMixin,
    extra_content_views.ExtraContentContractListView,
):
    template_name = 'common/training-contracts-dashboard.html'
    model = contracts_models.EducationContractsLogModel

class FreelanceContractsDashboardView(
    auth_mixins.LoginRequiredMixin,
    extra_content_views.ExtraContentContractListView,
):
    template_name = 'common/freelance-contracts-dashboard.html'
    model = contracts_models.FreelanceContractsLogModel

class FreelanceLectureContractsDashboardView(
    auth_mixins.LoginRequiredMixin,
    extra_content_views.ExtraContentContractListView,
):
    template_name = 'common/freelance-lecturers-contracts-dashboard.html'
    model = contracts_models.FreelanceLectureContractsLogModel
