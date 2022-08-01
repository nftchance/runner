from rest_framework import permissions, viewsets

from .models import Org
from .permissions import IsOrgAdmin, IsOrgMember
from .serializers import OrgSerializer


class OrgViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    lookup_url_kwarg = "org_id"

    queryset = Org.objects.all()
    serializer_class = OrgSerializer

    permission_classes = [permissions.IsAuthenticated, IsOrgMember]

    # Allow only admins to create new orgs and any other user to view 
    # the orgs they are customers of.
    def get_permissions(self):
        admin_actions = ["update", "destroy"]
        
        if self.action in admin_actions:
            self.permission_classes.append(IsOrgAdmin)

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)