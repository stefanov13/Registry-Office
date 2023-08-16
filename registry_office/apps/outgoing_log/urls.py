from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.OutgoingLogCreateView.as_view(), name='outgoing-create'),
    path('<int:pk>/', include([
        path('details/', views.OutgoingLogDetailsView.as_view(), name='outgoing-details'),
        path('edit/', views.OutgoingLogEditView.as_view(), name='outgoing-edit'),
        path('delete/', views.OutgoingLogDeleteView.as_view(), name='outgoing-delete'),
    ]))
]
