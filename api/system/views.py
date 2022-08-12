from rest_framework import mixins, viewsets

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
    queryset = WaitlistEntry.objects.all()
    serializer_class = WaitlistEntrySerializer