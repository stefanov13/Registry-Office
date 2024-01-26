from django.urls import path
from . import views


urlpatterns = [
    path('', views.BaseNewsFeedView.as_view(), name='index'),
    path('employees-id-dashboard/', views.EmployeePositionsIdView.as_view(), name='positions-id-dashboard'),
    path('outgoing-dashboard/', views.OutgoingDashboardView.as_view(), name='outgoing-dashboard'),
    path('incoming-dashboard/', views.IncomingDashboardView.as_view(), name='incoming-dashboard'),
    path('orders-dashboard/', views.OrdersDashboardView.as_view(), name='orders-dashboard'),
    path(
        'gen-contracts-dashboard/',
        views.GeneralContractsDashboardView.as_view(),
        name='gen-contracts-dashboard'
    ),
    path(
        'training-contracts-dashboard/',
        views.EducationContractsDashboardView.as_view(),
        name='training-contracts-dashboard'
    ),
    path(
        'freelance-contracts-dashboard/',
        views.FreelanceContractsDashboardView.as_view(),
        name='freelance-contracts-dashboard'
    ),
    path(
        'freelance-lecturers-contracts-dashboard/',
        views.FreelanceLectureContractsDashboardView.as_view(),
        name='freelance-lecturers-contracts-dashboard'
    ),
]
