from django.urls import path, include
from .views import NewsFeedCreateView, NewsFeedDetailsView, NewsFeedEditView, NewsFeedDeleteView


urlpatterns = [
    path('create/', NewsFeedCreateView.as_view(), name='news-create'),
    path('<int:pk>/', include([
        path('details/', NewsFeedDetailsView.as_view(), name='news-details'),
        path('edit/', NewsFeedEditView.as_view(), name='news-edit'),
        path('delete/', NewsFeedDeleteView.as_view(), name='news-delete'),
    ]))
]

