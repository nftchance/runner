from rest_framework.schemas import get_schema_view

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

schema_view = get_schema_view(
    title="runner",
    description="Backend REST API for runner",
    version="0.1",
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('coin.urls')),
    path('', include('governance.urls')),
    path('', include('job.urls')),
    path('', include('user.urls')),
    path('', include('org.urls')),
    path('', include('system.urls')),
    path('docs/', TemplateView.as_view(
        template_name='docs.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='docs'),
    path('openapi', schema_view, name='openapi-schema'),
]