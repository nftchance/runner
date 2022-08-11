from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'system/broadcast', views.BroadcastViewSet, basename='broadcast')

urlpatterns = router.urls