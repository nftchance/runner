import re

from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Broadcast, WaitlistEntry
from .serializers import BroadcastSerializer, WaitlistEntrySerializer

class BroadcastViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Broadcast.objects.all().exclude(expired_at__isnull=False)
    serializer_class = BroadcastSerializer

class WaitlistEntryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    lookup_field = "id"
    lookup_url_kwarg = "waitlist_entry_id"

    queryset = WaitlistEntry.objects.all()
    serializer_class = WaitlistEntrySerializer

    @action(detail=True, methods=['post'])
    def accept(self, request, waitlist_entry_id=None):
        entry = self.get_object()

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not entry.can_accept():
            return Response(
                {'detail': 'Waitlist redemption limit reached'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if entry.accepted_at:
            return Response(
                {'detail': 'Already accepted'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.user.email != entry.email:
            return Response(
                {'detail': 'Invite email does not match user email'},
                status=status.HTTP_400_BAD_REQUEST
            )

        entry.accept(request.user)
        return Response({"message": "You have accepted the waitlist entry."})