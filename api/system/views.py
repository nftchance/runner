from rest_framework import mixins, viewsets

from .models import Broadcast
from .serializers import BroadcastSerializer

class BroadcastViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Broadcast.objects.all().exclude(expired_at__isnull=False)
    serializer_class = BroadcastSerializer