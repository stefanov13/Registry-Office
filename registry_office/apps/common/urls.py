from django.urls import path
from django.views import generic as views


urlpatterns = [
    path('', views.TemplateView.as_view(template_name = 'common/index.html'), name='index'),

]