from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView # new

from . import views

urlpatterns = [
    path('user/sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('user/log_in/', views.LogInView.as_view(), name='log_in'),
    path('user/log_out/', views.LogOutView.as_view(), name='log_out'),
    path('user/logout_all/', views.LogoutAllView.as_view(), name='logout_all'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/<int:user_id>/', views.UpdateProfileView.as_view(), name='update_user'),
    path('user/change_password/<int:user_id>/', views.ChangePasswordView.as_view(), name='change_password'),
]