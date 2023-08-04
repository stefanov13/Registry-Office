from django.urls import path
from .views import BaseNewsFeedView, OutgoingDashboardView, IncomingDashboardView


urlpatterns = [
    path('', BaseNewsFeedView.as_view(), name='index'),
    path('outgoing-dashboard/', OutgoingDashboardView.as_view(), name='outgoing-dashboard'),
    path('incoming-dashboard/', IncomingDashboardView.as_view(), name='incoming-dashboard'),
]
