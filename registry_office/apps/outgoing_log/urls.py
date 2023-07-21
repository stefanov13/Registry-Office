from django.urls import path
from .views import OutgoingLogCreateView

urlpatterns = [
    path('create/', OutgoingLogCreateView.as_view(), name='outgoing-create'),
]
