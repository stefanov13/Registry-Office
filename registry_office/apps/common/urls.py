from django.urls import path
from django.views import generic as views
from .views import OutgoingDashboardView, IncomingDashboardView


urlpatterns = [
    path('', views.TemplateView.as_view(template_name = 'common/index.html'), name='index'),
    path('outgoing-dashboard/', OutgoingDashboardView.as_view(), name='outgoing-dashboard'),
    path('incoming-dashboard/', IncomingDashboardView.as_view(), name='incoming-dashboard'),
]
