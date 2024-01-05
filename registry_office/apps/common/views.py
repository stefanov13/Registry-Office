import os
from django.http import HttpResponse
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from core.mixins.moderator_group_mixin import GroupRequiredMixin
from ..news_feed.models import NewsFeedModel
from ..user_profiles.models import EmployeePositionsModel
from ..incoming_log.models import IncomingLogModel
from ..outgoing_log.models import OutgoingLogModel
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
        context['rows_per_page'] = self.request.GET.get('rows_per_page', 10)

        return context
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('rows_per_page', 10)
    
class EmployeePositionsIdView(
    auth_mixins.LoginRequiredMixin,
    GroupRequiredMixin,
    views.ListView,
):
    template_name = 'common/system-management.html'
    model = EmployeePositionsModel
    
    allowed_groups = [
        'admin',
        'administrative_manager',
        'document_controller',
    ]
    
    def get_queryset(self):
        return self.model.objects.order_by('-pk')

class IncomingDashboardView(
    auth_mixins.LoginRequiredMixin,
    views.ListView
):
    template_name = 'common/incoming-dashboard.html'
    model = IncomingLogModel

    allowed_groups = [
        'admin',
        'administrative_manager',
        'document_controller',
    ]   

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        current_user_ids = self.request.user.profile.employeepositionsmodel_set.all()
        current_user_groups = self.request.user.groups.values_list('name', flat=True)

        search = self.request.GET.get('search', '')

        rights = [
            set(current_user_groups).intersection(set(self.allowed_groups)),
            self.request.user.is_superuser,
            self.request.user.is_staff
        ]
        
        if any(rights):
            queryset = self.model.objects.filter(
                title__icontains=search
            ).order_by('-creation_date', '-log_num')

        else:
            queryset = self.model.objects.filter(
                responsible_employees__in=current_user_ids,
                title__icontains=search
            ).order_by('-creation_date', '-log_num')

        return queryset
    
    def get(self, request, *args, **kwargs):
        if 'export' in request.GET:
            # If 'export' parameter is present in the query string, export data
            return self.export_data()
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search'] = self.request.GET.get('search', '')
        context['rows_per_page'] = self.request.GET.get('rows_per_page', 10)

        # documents = context['object_list']

        # for document in documents:
        #     document.document_file = os.path.basename(document.document_file.name)

        return context
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('rows_per_page', 10)
    
    def export_data(self):
        # Retrieve the queryset
        queryset = self.get_queryset()

        # Create a new workbook and add a worksheet
        workbook = Workbook()
        worksheet = workbook.active

        # Write headers to the worksheet
        headers = [str(field.verbose_name) for field in IncomingLogModel._meta.fields]
        worksheet.append(headers)

        # Write data to the worksheet
        for obj in queryset:
            row = [str(getattr(obj, field.name)) for field in IncomingLogModel._meta.fields]
            worksheet.append(row)

        # Create a response with the Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=incoming_exported_data.xlsx'
        workbook.save(response)

        return response

class OutgoingDashboardView(
    auth_mixins.LoginRequiredMixin,
    views.ListView
):
    template_name = 'common/outgoing-dashboard.html'
    model = OutgoingLogModel

    allowed_groups = [
        'admin',
        'administrative_manager',
        'document_controller',
    ]

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        current_user_ids = self.request.user.profile.employeepositionsmodel_set.all()
        current_user_groups = self.request.user.groups.values_list('name', flat=True)

        search = self.request.GET.get('search', '')

        rights = [
            set(current_user_groups).intersection(set(self.allowed_groups)),
            self.request.user.is_superuser,
            self.request.user.is_staff
        ]

        if any(rights):
            queryset = self.model.objects.filter(
                title__icontains=search
            ).order_by('-creation_date', '-log_num')

        else:
            queryset = self.model.objects.filter(
                signatory_employee_id__in=current_user_ids,
                title__icontains=search
            ).order_by('-creation_date', '-log_num')

        return queryset
    
    def get(self, request, *args, **kwargs):
        if 'export' in request.GET:
            # If 'export' parameter is present in the query string, export data
            return self.export_data()
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search'] = self.request.GET.get('search', '')
        context['rows_per_page'] = self.request.GET.get('rows_per_page', 10)

        # documents = context['object_list']

        # for document in documents:
        #     document.document_file = os.path.basename(document.document_file.name)

        return context
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('rows_per_page', 10)
    
    def export_data(self):
        # Retrieve the queryset
        queryset = self.get_queryset()

        # Create a new workbook and add a worksheet
        workbook = Workbook()
        worksheet = workbook.active

        # Write headers to the worksheet
        headers = [str(field.verbose_name) for field in OutgoingLogModel._meta.fields]
        worksheet.append(headers)

        # Write data to the worksheet
        for obj in queryset:
            row = [str(getattr(obj, field.name)) for field in OutgoingLogModel._meta.fields]
            worksheet.append(row)

        # Create a response with the Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=outgoing_exported_data.xlsx'
        workbook.save(response)

        return response
