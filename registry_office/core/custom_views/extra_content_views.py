import re
from django.views import generic as views
from django.utils import timezone
from django.http import HttpResponse
from openpyxl import Workbook


class ExtraContentListView(views.ListView):
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
            self.request.user.is_staff,
        ]

        if any(rights):            
            queryset = self.model.objects.filter(
                title__icontains=search
            ).order_by('-creation_date__date', '-log_num', '-sub_log_num')

        else:
            queryset = self.model.objects.filter(
                concerned_employees__in=current_user_ids,
                title__icontains=search
            ).order_by('-creation_date__date', '-log_num', '-sub_log_num')

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

class ExtraContentCreateView(views.CreateView):

    def form_valid(self, form):
        form.instance.creator_user = self.request.user.profile
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        last_instance = self.model.objects.order_by('-creation_date__date', '-log_num').first()

        current_year = timezone.now().year

        if last_instance and last_instance.creation_date.year == current_year:
            last_log_num = last_instance.log_num
        else:
            last_log_num = 0

        next_log_num = last_log_num + 1

        context['next_log_num'] = next_log_num
        context['current_date'] = timezone.now

        return context
