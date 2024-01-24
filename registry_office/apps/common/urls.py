from django.urls import path
from . import views


urlpatterns = [
    path('', views.BaseNewsFeedView.as_view(), name='index'),
    path('system-management/', views.EmployeePositionsIdView.as_view(), name='positions-id-dashboard'),
    path('outgoing-dashboard/', views.OutgoingDashboardView.as_view(), name='outgoing-dashboard'),
    path('incoming-dashboard/', views.IncomingDashboardView.as_view(), name='incoming-dashboard'),
    path('orders-dashboard/', views.OrdersDashboardView.as_view(), name='orders-dashboard'),
    path('gen-contracts-dashboard/', views.GeneralContractsDashboardView.as_view(), name='gen-contracts-dashboard'),
]
