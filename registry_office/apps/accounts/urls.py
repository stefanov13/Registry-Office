from django.urls import path
from .views import RegisterUserView, UserLoginView


urlpatterns = [
    path('signup/', RegisterUserView.as_view, name='register-user'),
    path('login/', UserLoginView.as_view, name='login'),
    
]
