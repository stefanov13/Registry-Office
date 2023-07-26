import os
from django.shortcuts import render
from django.views import generic as view
from ..outgoing_log.models import OutgoingLogModel

# Create your views here.


# class BaseTemplateView(view.TemplateView):
#     template_name = 'common/index.html'


class OutgoingDashboardView(view.ListView):
    template_name = 'common/outgoing-dashboard.html'
    model = OutgoingLogModel

    def get_queryset(self):
        # Order items by primary key in descending order
        return self.model.objects.order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Modify the 'document_img' field in the context to display only the file name
        documents = context['object_list']
        for document in documents:
            document.document_img = os.path.basename(document.document_img.name)

        return context
