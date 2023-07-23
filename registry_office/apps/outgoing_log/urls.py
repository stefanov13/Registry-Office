from django.urls import path, include
from .views import OutgoingLogCreateView, OutgoingLogDetailsView, OutgoingLogEditView, OutgoingLogDeleteView

urlpatterns = [
    path('create/', OutgoingLogCreateView.as_view(), name='outgoing-create'),
    path('<int:pk>/', include([
        path('details/', OutgoingLogDetailsView.as_view(), name='outgoing-details'),
        path('edit/', OutgoingLogEditView.as_view(), name='outgoing-edit'),
        path('delete/', OutgoingLogDeleteView.as_view(), name='outgoing-delete'),
    ]))
]
