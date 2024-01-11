from django.views import generic as views

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
