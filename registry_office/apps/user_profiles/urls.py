from django.urls import path, include
from . import views

urlpatterns = [
    path('employee-id/create/', views.EmployeePositionsCreateView.as_view(), name='employee-pos-create'),
    path('<int:pk>/', include([
        path('employee-id/details/', views.EmployeePositionsDetailsView.as_view(), name='employee-pos-details'),
        path('employee-id/edit/', views.EmployeePositionsEditView.as_view(), name='employee-pos-edit'),
        path('employee-id/delete/', views.EmployeePositionsDeleteView.as_view(), name='employee-pos-delete'),
    ]))
]
