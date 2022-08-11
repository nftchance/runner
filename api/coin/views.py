from rest_framework import mixins, permissions, viewsets, filters

from .models import Transfer
from .serializers import TransferSerializer


class TransferViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = "id"
    lookup_url_kwarg = "transfer_id"

    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (filters.OrderingFilter, filters.SearchFilter)

    ordering_fields = '__all__'
    search_fields = ('id', 'label', 'amount', 'settled')
    filterset_fields = ('id', 'label', 'amount', 'settled')
