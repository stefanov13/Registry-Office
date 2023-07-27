from django.urls import path
from .views import BaseTemplateView, OutgoingDashboardView, IncomingDashboardView


urlpatterns = [
    path('', BaseTemplateView.as_view(), name='index'),
    path('outgoing-dashboard/', OutgoingDashboardView.as_view(), name='outgoing-dashboard'),
    path('incoming-dashboard/', IncomingDashboardView.as_view(), name='incoming-dashboard'),
]
