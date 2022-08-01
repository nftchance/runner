from rest_framework import generics, permissions, viewsets # changed
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Org 
from .serializers import OrgSerializer

class OrgView(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'id'
    lookup_url_kwarg = 'org_id'
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Org.objects.all()
    serializer_class = OrgSerializer 
