from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView # new

from . import views

urlpatterns = [
    path('user/sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('user/log-in/', views.LogInView.as_view(), name='log-in'),
    path('user/log-out/', views.LogOutView.as_view(), name='log-out'),
    path('user/log-out-all/', views.LogoutAllView.as_view(), name='log-out-all'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('user/<int:user_id>/', views.UpdateProfileView.as_view(), name='update-user'),
    path('user/password/<int:user_id>/', views.ChangePasswordView.as_view(), name='update-password'),
]