from django.urls import path
from .views import RegisterUserView, UserLoginView, UserLogoutView, UserDetailsView


urlpatterns = [
    path('signup/', RegisterUserView.as_view(), name='register-user'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('details/', UserDetailsView.as_view(), name='user-details'),

]
