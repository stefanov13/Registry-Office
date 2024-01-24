from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.GeneralContractsLogCreateView.as_view(), name='gen-contracts-create'),
#     path('freelance-create/', views.LogCreateView.as_view(), name='freelance-contracts-create'),
#     path('freelance-lecturers-create/', views.LogCreateView.as_view(), name='freelance-lecturers-contracts-create'),
#     path('training-create/', views.LogCreateView.as_view(), name='training-contracts-create'),
    path('<int:pk>/', include([
        path('details/', views.GeneralContractsLogDetailsView.as_view(), name='gen-contracts-details'),
        path('edit/', views.GeneralContractsLogEditView.as_view(), name='gen-contracts-edit'),
        path('delete/', views.GeneralContractsLogDeleteView.as_view(), name='gen-contracts-delete'),
#         path('freelance-details/', views.LogDetailsView.as_view(), name='freelance-contracts-details'),
#         path('freelance-edit/', views.LogEditView.as_view(), name='freelance-contracts-edit'),
#         path('freelance-delete/', views.LogDeleteView.as_view(), name='freelance-contracts-delete'),
#         path('freelance-lecturers-details/', views.LogDetailsView.as_view(), name='freelance-lecturers-contracts-details'),
#         path('freelance-lecturers-edit/', views.LogEditView.as_view(), name='freelance-lecturers-contracts-edit'),
#         path('freelance-lecturers-delete/', views.LogDeleteView.as_view(), name='freelance-lecturers-contracts-delete'),
#         path('training-details/', views.LogDetailsView.as_view(), name='training-contracts-details'),
#         path('training-edit/', views.LogEditView.as_view(), name='training-contracts-edit'),
#         path('training-delete/', views.LogDeleteView.as_view(), name='training-contracts-delete'),
    ]))
]
