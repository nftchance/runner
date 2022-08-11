from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('coin.urls')),
    path('', include('governance.urls')),
    path('', include('job.urls')),
    path('', include('user.urls')),
    path('', include('org.urls')),
    path('', include('system.urls'))
]
