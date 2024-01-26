from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.GeneralContractsLogCreateView.as_view(), name='gen-contracts-create'),
    path('type-create/', views.ContractTypesCreateView.as_view(), name='contract-types-create'),
    path('freelance-create/', views.FreelanceContractsLogCreateView.as_view(), name='freelance-contracts-create'),
    path('freelance-lecturers-create/', views.FreelanceLectureContractsLogCreateView.as_view(), name='freelance-lecturers-contracts-create'),
    path('training-create/', views.EducationContractsLogCreateView.as_view(), name='training-contracts-create'),
    path('<int:pk>/', include([
        path('type-edit/', views.ContractTypesEditView.as_view(), name='contract-types-edit'),
        path('type-delete/', views.ContractTypesDeleteView.as_view(), name='contract-types-delete'),
        path('details/', views.GeneralContractsLogDetailsView.as_view(), name='gen-contracts-details'),
        path('edit/', views.GeneralContractsLogEditView.as_view(), name='gen-contracts-edit'),
        path('delete/', views.GeneralContractsLogDeleteView.as_view(), name='gen-contracts-delete'),
        path('freelance-details/', views.FreelanceContractsLogDetailsView.as_view(), name='freelance-contracts-details'),
        path('freelance-edit/', views.FreelanceContractsLogEditView.as_view(), name='freelance-contracts-edit'),
        path('freelance-delete/', views.FreelanceContractsLogDeleteView.as_view(), name='freelance-contracts-delete'),
        path('freelance-lecturers-details/', views.FreelanceLectureContractsLogDetailsView.as_view(), name='freelance-lecturers-contracts-details'),
        path('freelance-lecturers-edit/', views.FreelanceLectureContractsLogEditView.as_view(), name='freelance-lecturers-contracts-edit'),
        path('freelance-lecturers-delete/', views.FreelanceLectureContractsLogDeleteView.as_view(), name='freelance-lecturers-contracts-delete'),
        path('training-details/', views.EducationContractsLogDetailsView.as_view(), name='training-contracts-details'),
        path('training-edit/', views.EducationContractsLogEditView.as_view(), name='training-contracts-edit'),
        path('training-delete/', views.EducationContractsLogDeleteView.as_view(), name='training-contracts-delete'),
    ]))
]
