from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView # new

from . import views

router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user')

urlpatterns = [
    path('user/log-in/', views.LogInView.as_view(), name='log-in'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
] + router.urls