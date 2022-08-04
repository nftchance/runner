from django.shortcuts import get_object_or_404
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

    def get_queryset(self, *args, **kwargs):
        if self.action == "use_invitation":
            return Org.objects.filter(id=self.kwargs["org_id"])

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
        relationship, created = OrgRelationship.objects.get_or_create(
            org=obj, related_user=self.request.user
        )
        # assign the admin role
        role = OrgRole.objects.get_or_create(name=Role.ADMIN)[0]
        relationship.role = role
        relationship.save()

        # add this org to the users orgs
        self.request.user.org_relationships.add(relationship)
        self.request.user.save()

    @action(
        detail=True,
        methods=["post"],
        url_path="use_invitation/(?P<org_invitation_id>[^/.]+)",
        permission_classes=[permissions.IsAuthenticated],
    )
    def use_invitation(self, request, org_id=None, org_invitation_id=None):
        org_invitation = get_object_or_404(OrgInvitation, id=org_invitation_id)

        org = self.get_object()

        if org.pk in request.user.org_relationships.values_list("org__pk", flat=True):
            return Response(
                {"error": "You are already a member of this org."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if org_invitation.org != org:
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

    @action(
        detail=True,
        methods=["post"],
        url_path="revoke_invitation/(?P<org_invitation_id>[^/.]+)",
        permission_classes=[permissions.IsAuthenticated, CanManageOrgInvitiation],
    )
    def revoke_invitation(self, request, org_id=None, org_invitation_id=None):
        org_invitation = get_object_or_404(OrgInvitation, id=org_invitation_id)

        org = self.get_object()

        if org_invitation.org != org:
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


class OrgInvitationViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    lookup_url_kwarg = "org_invitation_id"

    serializer_class = OrgInvitationSerializer

    permission_classes = [permissions.IsAuthenticated, CanManageOrgInvitiation]

    def get_queryset(self, *args, **kwargs):
        return OrgInvitation.objects.filter(
            org__in=self.request.user.org_relationships.all().values_list(
                "org", flat=True
            )
        )

    # Allow only admins to see all, create, or destory invitiations however
    # any authenticated user can accept a pending invitation.
    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

    # when a new invitation is created check if the request user is an admin of the org
    # if not, then the response is a 403 error.
    def create(self, request, *args, **kwargs):
        # if request org not in request user orgs, then return 403
        if not request.user.org_relationships.filter(org=request.data["org"]).exists():
            return Response(
                {"error": "You are not an admin of this org."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(invited_by=self.request.user)
