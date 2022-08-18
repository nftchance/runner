import django

from django.db.models import Q

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Broadcast, WaitlistEntry
from .permissions import CanManageBroadcast, CanManageWaitlistEntry
from .serializers import BroadcastSerializer, WaitlistEntrySerializer


class BroadcastViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a Broadcast instance.

        permissions: 
            Request user must have manage_broadcast permission.
    list:
        Return a list of all Waitlist Entries.

        permissions: 
            Anyone can list the active Broadcast instances.
    create:
        Create a new Waitlist Entry.

        permissions: 
            Request user must have manage_broadcast permission.
    delete:
        Remove an existing Broadcast.

        permissions: 
            Request user must have manage_broadcast permission.
    partial_update:
        Update one or more fields on an existing Broadcast.

        permissions: 
            Request user must have manage_broadcast permission.
    update:
        Update a Broadcast.

        permissions: 
            Request user must have manage_broadcast permission.
    """

    queryset = Broadcast.objects.filter(Q(expired_at__isnull=True) | Q(expired_at__gt=django.utils.timezone.now())).distinct()
    serializer_class = BroadcastSerializer

    permission_classes = (permissions.AllowAny,)

    def get_permissions(self):
        if self.action not in ['list']:
            self.permission_classes = [CanManageBroadcast]

        return [permission() for permission in self.permission_classes]


class WaitlistEntryViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a Waitlist Entry instance.

        permissions: 
            Request user must have manage_waitlistentry permission.
    list:
        Return a list of all Waitlist Entries.

        permissions: 
            Request user must have manage_waitlistentry permission.
    create:
        Create a new Waitlist Entry.

        permissions: 
            Allow any, the email provided simply cannot be arleady in the waitlist. 
    delete:
        Remove an existing Waitlist Entry.

        permissions: 
            Request user must have manage_waitlistentry permission.
    partial_update:
        Update one or more fields on an existing Waitlist Entry.

        permissions: 
            Request user must have manage_waitlistentry permission.
    update:
        Update a Waitlist Entry.

        permissions: 
            Request user must have manage_waitlistentry permission.
    invite:
        Invite a user to become a user of runner.

        permissions:
            Request user must have manage_waitlistentry permission.
    accept: 
        Approve a Waitlist Entry that has been marked as an active invitation.

        permissions:
            User must be authenticated and not logged into an account that is already accepted.
    """
    lookup_field = "id"
    lookup_url_kwarg = "waitlist_entry_id"

    permission_classes = [permissions.AllowAny]

    queryset = WaitlistEntry.objects.all()
    serializer_class = WaitlistEntrySerializer

    def get_permissions(self):
        if self.action not in ["create", "accept"]:
            self.permission_classes = [CanManageWaitlistEntry]

        return [permission() for permission in self.permission_classes]

    @action(detail=True, methods=["post"])
    def invite(self, request, *args, **kwargs):
        waitlist_entry = self.get_object()

        if waitlist_entry.invited_at != None:
            return Response(
                {"detail": "Already invited"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        waitlist_entry.invite()

        serializer = self.get_serializer(waitlist_entry)

        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def accept(self, request, *args, **kwargs):
        entry = self.get_object()

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if WaitlistEntry.objects.filter(user=request.user, accepted_at__isnull=False).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Already accepted"})

        if not entry.can_accept():
            return Response(
                {'error': 'Waitlist redemption limit reached'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if entry.accepted_at:
            return Response(
                {'error': 'Already accepted'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.user.email != entry.email:
            return Response(
                {'email': 'Invite email does not match user email'},
                status=status.HTTP_400_BAD_REQUEST
            )

        entry.accept(request.user)

        serializer = self.get_serializer(entry)

        return Response(serializer.data)
