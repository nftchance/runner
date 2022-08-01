from rest_framework import permissions, viewsets

from .models import Org
from .permissions import IsOrgMember
from .serializers import OrgSerializer


class OrgView(viewsets.ReadOnlyModelViewSet):
    lookup_field = "id"
    lookup_url_kwarg = "org_id"

    permission_classes = (permissions.IsAuthenticated, IsOrgMember)

    queryset = Org.objects.all()
    serializer_class = OrgSerializer
