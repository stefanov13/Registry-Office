from django.http import Http404
from django.views import generic as views
from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.http import HttpResponse
from openpyxl import Workbook
from apps.contracts_log.models import ContractTypesModel


class ExtraContentListView(views.ListView):
    DEFAULT_FROM_DATE = '2023-01-01'

    allowed_groups = [
        'admin',
        'administrative_manager',
        'document_controller',
    ]

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        current_user_ids = self.request.user.profile.employeepositionsmodel_set.all()
        current_user_groups = self.request.user.groups.values_list('name', flat=True)

        self.current_date = timezone.now().date().strftime('%Y-%m-%d')

        self.selected_log_num = self.request.GET.get('log-num', '')
        self.search = self.request.GET.get('search', '')
        self.from_date = self.request.GET.get('from-date', self.DEFAULT_FROM_DATE)
        self.to_date = self.request.GET.get('to-date', self.current_date)

        self.from_date = parse_date(self.from_date)
        self.to_date = parse_date(self.to_date)

        if not self.from_date:
            self.from_date = self.DEFAULT_FROM_DATE

        if not self.to_date:
            self.to_date = self.current_date

        words = self.search.strip().split()

        # Build a Q object for each word
        query = Q()
        for word in words:
            query &= Q(title__icontains=word)

        rights = [
            set(current_user_groups).intersection(set(self.allowed_groups)),
            self.request.user.is_superuser,
            self.request.user.is_staff,
        ]

        if any(rights):            
            queryset = self.model.objects.filter(
                query,
                creation_date__date__gte=self.from_date,
                creation_date__date__lte=self.to_date
            ).order_by('-creation_date__date', '-log_num', '-sub_log_num')

        else:
            queryset = self.model.objects.filter(
                query,
                concerned_employees__in=current_user_ids,
                creation_date__date__gte=self.from_date,
                creation_date__date__lte=self.to_date
            ).order_by('-creation_date__date', '-log_num', '-sub_log_num')

        if int(self.selected_log_num) if self.selected_log_num.isdigit() else 0:
            queryset = queryset.filter(
                log_num=self.selected_log_num
            ).order_by('-creation_date__year', '-sub_log_num')

        return queryset
    
    def get(self, request, *args, **kwargs):
        if 'export' in request.GET:
            # If 'export' parameter is present in the query string, export data
            return self.export_data()
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['selected_log_num'] = self.selected_log_num
        context['search'] = self.search
        context['from_date'] = self.from_date.strftime('%Y-%m-%d') if not isinstance(self.from_date, str) else self.from_date
        context['to_date'] = self.to_date.strftime('%Y-%m-%d') if not isinstance(self.to_date, str) else self.to_date
        context['current_date'] = self.current_date
        context['rows_per_page'] = self.request.GET.get('rows_per_page', 8)

        # documents = context['object_list']

        # for document in documents:
        #     document.document_file = os.path.basename(document.document_file.name)

        return context
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('rows_per_page', 8)
    
    def export_data(self):
        # Retrieve the queryset
        queryset = self.get_queryset()

        # Create a new workbook and add a worksheet
        workbook = Workbook()
        worksheet = workbook.active

        # Write headers to the worksheet
        headers = []
        
        for field in self.model._meta.fields:
            headers.append(f'{field.verbose_name}') if field.is_relation else headers.append(str(field.verbose_name))

        worksheet.append(headers)

        # Write data to the worksheet
        for obj in queryset:
            row = []

            for field in self.model._meta.fields:
                row.append(str(getattr(obj, field.name))) if field.is_relation else row.append(str(getattr(obj, field.name)))

            worksheet.append(row)

        # Create a response with the Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={self.model._meta.app_label}_exported_data.xlsx'
        workbook.save(response)

        return response
    
class ExtraContentContractListView(ExtraContentListView):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        self.selected_type = self.request.GET.get('contract-type', 0)

        if bool(int(self.selected_type)):
            queryset = queryset.filter(
                contract_type=self.selected_type
            ).order_by('-log_num', '-sub_log_num')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['contract_types'] = ContractTypesModel.objects.all()
        context['selected_type'] = self.selected_type

        return context

class ExtraContentCreateView(views.CreateView):
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields[
            'concerned_employees'
        ].queryset = form.fields[
            'concerned_employees'
        ].queryset.order_by('pk')

        return form

    def form_valid(self, form):
        form.instance.creator_user = self.request.user.profile
        
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # last_instance = self.model.objects.order_by(
        #     '-creation_date__date',
        #     '-log_num'
        # ).first()

        current_year = timezone.now().year

        last_instance = self.model.objects.filter(
                creation_date__year=current_year
            ).order_by('-log_num').first()

        if last_instance and last_instance.creation_date.year == current_year:
            last_log_num = last_instance.log_num
        else:
            last_log_num = 0

        next_log_num = last_log_num + 1

        context['next_log_num'] = next_log_num
        context['current_date'] = timezone.now

        return context
