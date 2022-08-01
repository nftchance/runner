from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'org', views.OrgViewSet, basename='org')

urlpatterns = router.urls