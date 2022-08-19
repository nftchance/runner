from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Org, OrgInvitation, OrgRelationship
from .permissions import (
    CanManageOrg,
    CanManageOrgRelationship,
    CanManageOrgInvitiation,
)
from .serializers import (
    OrgSerializer,
    OrgRelationshipSerializer,
    OrgInvitationSerializer,
)

class OrgViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a Org.

        permissions: 
            Request user must have manage_org permission or be a member of the org.
    list:
        Return a list of all Orgs if request user has manage_org permission or orgs of the logged in user.

        permissions: 
            Request user must have manage_org permission or be a member of the org.
    create:
        Create a new Org.

        permissions: 
            Request user must be authenticated.
    delete:
        Delete an existing Org.

        permissions: 
            Request user must have manage_org permission as admin or org member.
    partial_update:
        Update one or more fields on an existing Org.

        permissions: 
            Request user must have manage_org permission as admin or org member.
    update:
        Update an Org.

        permissions: 
            Request user must have manage_org permission as admin or org member.
    """
    lookup_field = "id"
    lookup_url_kwarg = "org_id"

    serializer_class = OrgSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # if runner team member, can access all orgs
        if self.request.user.has_perm("org.manage_org"):
            return Org.objects.all()

        # return organizations of all relationships for request user
        relationships = self.request.user.org_relationships.all()
        return Org.objects.filter(relationships__in=relationships)

    # Allow only admins to create new orgs and any other user to view
    # the orgs they are customers of.
    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [permissions.IsAuthenticated, CanManageOrg]

        return [permission() for permission in self.permission_classes]

class OrgRelationshipViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    retrieve:
        Return a Org Relationship.

        permissions: 
            Request user must have manage_orgrelationship permission or be a member of the org.
    list:
        Return 
    
        permissions: 
            Request user must have manage_orgrelationship permission or be a member of the org.
    partial_update:
        Update one or more fields on an existing Org Relationship.

        permissions: 
            Request user must have manage_orgrelationship permission as admin or org member.
    update:
        Update an Org Relationship.

        permissions: 
            Request user must have manage_orgrelationship permission as admin or org member. 
    """
    lookup_field = "id"
    lookup_url_kwarg = "org_relationship_id"

    serializer_class = OrgRelationshipSerializer

    permission_classes = [permissions.IsAuthenticated, CanManageOrgRelationship]

    def get_queryset(self):
        if "org_relationship_id" in self.kwargs:
            return OrgRelationship.objects.filter(id=self.kwargs["org_relationship_id"])

        return OrgRelationship.objects.filter(org=self.kwargs["org_id"])


class OrgInvitationViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    lookup_url_kwarg = "org_invitation_id"

    serializer_class = OrgInvitationSerializer

    permission_classes = [permissions.IsAuthenticated, CanManageOrgInvitiation]

    def get_queryset(self):
        # when they are accepting an invitiation allow it with direct code only
        if self.action == "accept":
            return OrgInvitation.objects.filter(id=self.kwargs["org_invitation_id"])

        # return the invitations for the users organizations
        return OrgInvitation.objects.filter(
            org__in=self.request.user.org_relationships.all().values_list(
                "org", flat=True
            )
        )

    def perform_create(self, serializer):
        serializer.save(invited_by=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def accept(self, request, **kwargs):
        org_invitation = self.get_object()

        if request.user.org_relationships.filter(org__pk=kwargs["org_id"]).exists():
            return Response(
                {"error": "You are already a member of this org."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if org_invitation.org.pk != kwargs["org_id"]:
            return Response(
                {"error": "This invitation is not for this org."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if org_invitation.invited_user:
            return Response(
                {"error": "This invitation has already been used."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        org_invitation.accept(request.user)

        serializer = OrgInvitationSerializer(org_invitation)

        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def revoke(self, request, **kwargs):
        org_invitation = self.get_object()

        if org_invitation.org.pk != kwargs["org_id"]:
            return Response(
                {"error": "This invitation is not for this org."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if org_invitation.revoked_at:
            return Response(
                {"error": "This invitation has already been revoked."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        org_invitation.revoke()

        serializer = OrgInvitationSerializer(org_invitation)

        return Response(serializer.data)
