from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from core.mixins.moderator_group_mixin import GroupRequiredMixin
from core.custom_views.extra_content_views import ExtraContentListView
from ..news_feed.models import NewsFeedModel
from ..user_profiles.models import EmployeePositionsModel
from ..incoming_log.models import IncomingLogModel
from ..outgoing_log.models import OutgoingLogModel
from ..administrative_orders_log.models import AdministrativeOrdersLogModel
from ..contracts_log.models import GeneralContractsLogModel


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
    model = GeneralContractsLogModel
