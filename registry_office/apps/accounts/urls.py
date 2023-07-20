from django.urls import path, include
from .views import UserRegisterView, UserLoginView, UserLogoutView, UserDetailsView, UserEditView, UserDeleteView, UserChangePasswordView


urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name='register-user'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('user-details/', UserDetailsView.as_view(), name='user-details'),
    path('user-edit/', UserEditView.as_view(), name='user-edit'),
    path('user-delete/', UserDeleteView.as_view(), name='user-delete'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    # path('<int:pk>/', include([
        
    # ])),

]
