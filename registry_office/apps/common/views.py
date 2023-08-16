import os
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from ..news_feed.models import NewsFeedModel
from ..incoming_log.models import IncomingLogModel
from ..outgoing_log.models import OutgoingLogModel

# Create your views here.


class BaseNewsFeedView(views.ListView):
    template_name = 'common/index.html'
    model = NewsFeedModel

    def get_queryset(self):
        return self.model.objects.order_by('-date')
    

class IncomingDashboardView(auth_mixins.LoginRequiredMixin, views.ListView):
    template_name = 'common/incoming-dashboard.html'
    model = IncomingLogModel
    allowed_groups = ['admin', 'document_controller']   

    def get_queryset(self):
        current_user_profile = self.request.user.profile
        current_user_groups = self.request.user.groups.values_list('name', flat=True)
        rights = [
                set(current_user_groups).intersection(set(self.allowed_groups)),
                self.request.user.is_superuser,
                self.request.user.is_staff
            ]
        
        if any(rights):
            queryset = self.model.objects.order_by('-pk')
        else:
            queryset = self.model.objects.filter(responsible_people__in=[current_user_profile]).order_by('-pk')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Modify the 'document_img' field in the context to display only the file name
        documents = context['object_list']

        for document in documents:
            document.document_img = os.path.basename(document.document_img.name)

        return context

class OutgoingDashboardView(auth_mixins.LoginRequiredMixin, views.ListView):
    template_name = 'common/outgoing-dashboard.html'
    model = OutgoingLogModel
    allowed_groups = ['admin', 'document_controller']

    def get_queryset(self):
        current_user_profile = self.request.user.profile
        current_user_groups = self.request.user.groups.values_list('name', flat=True)
        rights = [
                set(current_user_groups).intersection(set(self.allowed_groups)),
                self.request.user.is_superuser,
                self.request.user.is_staff
            ]

        if any(rights):
            queryset = self.model.objects.order_by('-pk')
        else:
            queryset = self.model.objects.filter(signatory_profile=current_user_profile).order_by('-pk')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Modify the 'document_img' field in the context to display only the file name
        documents = context['object_list']
        
        for document in documents:
            document.document_img = os.path.basename(document.document_img.name)

        return context

