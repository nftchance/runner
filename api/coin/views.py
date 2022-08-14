from django.db.models import Q

from rest_framework import mixins, permissions, viewsets, filters

from .models import Transfer
from .permissions import CanManageTransfer
from .serializers import TransferSerializer


class TransferViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    lookup_url_kwarg = "transfer_id"

    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    # permission_classes = [permissions.AllowAny]

    filter_backends = (filters.OrderingFilter, filters.SearchFilter)

    ordering_fields = '__all__'
    search_fields = ('id', 'label', 'amount', 'settled')
    filterset_fields = ('id', 'label', 'amount', 'settled')

    def get_queryset(self):
        if self.request.user.has_perm('coin.manage_transfer'):
            return self.get_queryset.all()

        # only return transfers that were to or from request.user
        return self.queryset.filter(
            Q(from_user=self.request.user) | Q(to_user=self.request.user)
        )

    # implement the ability for users with manage_transfer perm to create, update, and delete transfers
    def get_permissions(self):
        if self.action not in ['list', 'retrieve']:
            self.permission_classes = [CanManageTransfer]

        return [permission() for permission in self.permission_classes]