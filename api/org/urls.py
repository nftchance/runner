from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'org', views.OrgViewSet, basename='org')
router.register(r'org/(?P<org_id>[^/.]+)/org-relationship', views.OrgRelationshipViewSet, basename='org-relationship')
router.register(r'org/(?P<org_id>[^/.]+)/org-invitation', views.OrgInvitationViewSet, basename='org-invitation')

urlpatterns = router.urls