from rest_framework import generics, permissions, viewsets # changed
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Job 
from .serializers import JobSerializer

class JobView(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'id'
    lookup_url_kwarg = 'job_id'

    permission_classes = (permissions.IsAuthenticated,)

    queryset = Job.objects.all()
    serializer_class = JobSerializer 
