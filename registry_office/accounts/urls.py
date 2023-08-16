from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.UserRegisterView.as_view(), name='register-user'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('user-details/', views.UserDetailsView.as_view(), name='user-details'),
    path('user-edit/', views.UserEditView.as_view(), name='user-edit'),
    path('user-delete/', views.UserDeleteView.as_view(), name='user-delete'),
    path('change-password/', views.UserChangePasswordView.as_view(), name='change-password'),
]
