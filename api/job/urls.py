from django.urls import path

from . import views

urlpatterns = [
    path('api/job/', views.JobView.as_view({'get': 'list'}), name='job_list'),
    path('api/job/<job_id>/', views.JobView.as_view({'get': 'retrieve'}), name='job_detail'),  # new
]