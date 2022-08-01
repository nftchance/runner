from rest_framework import permissions, viewsets

from .models import Org
from .permissions import IsOrgAdmin, IsOrgMember
from .serializers import OrgSerializer


class OrgViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    lookup_url_kwarg = "org_id"

    serializer_class = OrgSerializer

    permission_classes = [permissions.IsAuthenticated, IsOrgMember]

    def get_queryset(self, *args, **kwargs):
        return self.request.user.orgs.all()

    # Allow only admins to create new orgs and any other user to view 
    # the orgs they are customers of.
    def get_permissions(self):
        admin_actions = ["update", "destroy"]
        
        if self.action in admin_actions:
            self.permission_classes.append(IsOrgAdmin)

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        # save the new org into the database
        obj = serializer.save(admin=self.request.user)

        # add this org to the users orgs
        self.request.user.orgs.add(obj)
        self.request.user.save()