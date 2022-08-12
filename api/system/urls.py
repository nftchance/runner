from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'system/broadcast', views.BroadcastViewSet, basename='broadcast')
router.register(r'system/waitlist', views.WaitlistEntryViewSet, basename='waitlist')

urlpatterns = router.urls