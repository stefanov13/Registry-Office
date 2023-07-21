from django.shortcuts import render
from django.views import generic as view
from ..outgoing_log.models import OutgoingLogModel

# Create your views here.


# class BaseTemplateView(view.TemplateView):
#     template_name = 'common/index.html'


class OutgoingDashboardView(view.ListView):
    template_name = 'common/outgoing-dashboard.html'
    model = OutgoingLogModel
