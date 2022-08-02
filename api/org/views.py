from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Org, OrgInvitation
from .permissions import IsOrgAdmin, IsOrgMember, IsOrgMemberForInvitation
from .serializers import OrgSerializer, OrgInvitationSerializer


class OrgViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    lookup_url_kwarg = "org_id"

    serializer_class = OrgSerializer

    permission_classes = [permissions.IsAuthenticated, IsOrgMember]

    def get_queryset(self, *args, **kwargs):
        if self.action == 'use_invitation':
            return Org.objects.filter(id=self.kwargs['org_id'])
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

    @action(
        detail=True,
        methods=["post"],
        url_path="use_invitation/(?P<org_invitation_id>[^/.]+)",
        permission_classes=[permissions.IsAuthenticated]
    )
    def use_invitation(self, request, org_id=None, org_invitation_id=None):
        org_invitation = get_object_or_404(OrgInvitation, id=org_invitation_id)

        org = self.get_object()

        if org in request.user.orgs.all():
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
        permission_classes=[permissions.IsAuthenticated, IsOrgAdmin]
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

    permission_classes = [permissions.IsAuthenticated, IsOrgMemberForInvitation]

    def get_queryset(self, *args, **kwargs):
        return OrgInvitation.objects.filter(org__in=self.request.user.orgs.all())

    # Allow only admins to see all, create, or destory invitiations however
    # any authenticated user can accept a pending invitation.
    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

    # when a new invitation is created check if the request user is an admin of the org
    # if not, then the response is a 403 error.
    def create(self, request, *args, **kwargs):
        # if request org not in request user orgs, then return 403
        if not request.user.orgs.filter(id=request.data["org"]).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(invited_by=self.request.user)
