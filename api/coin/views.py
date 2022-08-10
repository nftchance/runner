from rest_framework import mixins, permissions, viewsets

from .models import Transfer
from .serializers import TransferSerializer


class TransferViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = "id"
    lookup_url_kwarg = "transfer_id"

    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
