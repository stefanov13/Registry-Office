from django.urls import path, include
from .views import IncomingLogCreateView, IncomingLogDetailsView, IncomingLogEditView, IncomingLogDeleteView

urlpatterns = [
    path('create/', IncomingLogCreateView.as_view(), name='incoming-create'),
    path('<int:pk>/', include([
        path('details/', IncomingLogDetailsView.as_view(), name='incoming-details'),
        path('edit/', IncomingLogEditView.as_view(), name='incoming-edit'),
        path('delete/', IncomingLogDeleteView.as_view(), name='incoming-delete'),
    ]))
]
