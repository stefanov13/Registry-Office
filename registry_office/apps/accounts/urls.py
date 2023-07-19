from django.urls import path, include
from .views import RegisterUserView, UserLoginView, UserLogoutView, UserDetailsView, UserEditView, UserDeleteView, UserChangePasswordView


urlpatterns = [
    path('signup/', RegisterUserView.as_view(), name='register-user'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('details/', UserDetailsView.as_view(), name='user-details'),
    path('<int:pk>/', include([
        path('edit/', UserEditView.as_view(), name='user-edit'),
        path('delete/', UserDeleteView.as_view(), name='user-delete'),
        path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    ])),

]
