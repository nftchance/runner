from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Org, OrgInvitation, OrgRelationship, OrgRole
from .permissions import CanManageOrg, CanViewOrg, CanManageOrgInvitiation
from .serializers import OrgSerializer, OrgInvitationSerializer
from .utils import Role


class OrgViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    lookup_url_kwarg = "org_id"

    serializer_class = OrgSerializer

    permission_classes = [permissions.IsAuthenticated, CanViewOrg]

    def get_queryset(self):
        # return organizations of all relationships for request user
        relationships = self.request.user.org_relationships.all()
        return Org.objects.filter(relationships__in=relationships)

    # Allow only admins to create new orgs and any other user to view
    # the orgs they are customers of.
    def get_permissions(self):
        admin_actions = ["update", "destroy"]

        if self.action in admin_actions:
            self.permission_classes.append(CanManageOrg)

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        # save the new org into the database
        obj = serializer.save()

        # create admin relationship object
        relationship = OrgRelationship.objects.get_or_create(
            org=obj, related_user=self.request.user
        )[0]
        # assign the admin role
        role = OrgRole.objects.get_or_create(name=Role.ADMIN)[0]
        relationship.role = role
        relationship.save()

        # add this org to the users orgs
        self.request.user.org_relationships.add(relationship)
        self.request.user.save()


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

        if org_invitation.org.pk in request.user.org_relationships.values_list(
            "org__pk", flat=True
        ):
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
