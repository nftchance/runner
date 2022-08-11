from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'proposal', views.ProposalViewSet, basename='proposal')

urlpatterns = [
    path('proposal/(<int:proposal_id>/vote/', views.ProposalVoteView.as_view(), name='proposal-vote')

] + router.urls