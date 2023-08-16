from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.IncomingLogCreateView.as_view(), name='incoming-create'),
    path('person-opinion/edit/<int:pk>', views.PersonOpinionEditView.as_view(), name='person-opinion-edit'),
    path('person-opinion/delete/<int:pk>', views.PersonOpinionDeleteView.as_view(), name='person-opinion-delete'),
    path('<int:pk>/', include([
        path('details/', views.IncomingLogDetailsView.as_view(), name='incoming-details'),
        path('edit/', views.IncomingLogEditView.as_view(), name='incoming-edit'),
        path('delete/', views.IncomingLogDeleteView.as_view(), name='incoming-delete'),
    ]))
]
