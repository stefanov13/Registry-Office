from django.urls import path, include
from . import views


urlpatterns = [
    path('create/', views.NewsFeedCreateView.as_view(), name='news-create'),
    path('<int:pk>/', include([
        path('details/', views.NewsFeedDetailsView.as_view(), name='news-details'),
        path('edit/', views.NewsFeedEditView.as_view(), name='news-edit'),
        path('delete/', views.NewsFeedDeleteView.as_view(), name='news-delete'),
    ]))
]

