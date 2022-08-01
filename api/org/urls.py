from django.urls import path

from . import views

urlpatterns = [
    path('api/org/', views.OrgView.as_view({'get': 'list'}), name='org_list'),
    path('api/org/<org_id>/', views.OrgView.as_view({'get': 'retrieve'}), name='org_detail'),  # new
]