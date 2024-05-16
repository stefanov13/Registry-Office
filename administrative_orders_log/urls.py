from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.AdministrativeOrdersLogCreateView.as_view(), name='orders-create'),
    path('<int:pk>/', include([
        path('details/', views.AdministrativeOrdersLogDetailsView.as_view(), name='orders-details'),
        path('edit/', views.AdministrativeOrdersLogEditView.as_view(), name='orders-edit'),
        path('delete/', views.AdministrativeOrdersLogDeleteView.as_view(), name='orders-delete'),
    ]))
]
