import re

from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Broadcast, WaitlistEntry
from .permissions import CanManageBroadcast, CanManageWaitlistEntry
from .serializers import BroadcastSerializer, WaitlistEntrySerializer


class BroadcastViewSet(viewsets.ModelViewSet):
    queryset = Broadcast.objects.all().exclude(expired_at__isnull=False)
    serializer_class = BroadcastSerializer

    permission_classes = (permissions.AllowAny,)

    def get_permissions(self):
        if self.action not in ['list']:
            self.permission_classes = [CanManageBroadcast]

        return [permission() for permission in self.permission_classes]


class WaitlistEntryViewSet(viewsets.ModelViewSet):
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
