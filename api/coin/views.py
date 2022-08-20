from django.db.models import Q

from rest_framework import filters, permissions, viewsets

from .models import Transfer
from .permissions import CanManageTransfer
from .serializers import TransferSerializer


class TransferViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a Transfer instance.

        permissions: 
            Must be party of transfer or have manage_transfer permission.
    list:
        Return all Transfers user has access to viewing, ordered by most recent to oldest.

        permissions: 
            Must be party of transfer or have manage_transfer permission.
    create:
        Create a new Transfer.

        permissions: 
            Must have manage_transfer permission.
    delete:
        Remove an existing Transfer.

        permissions: 
            Must have manage_transfer permission.
    partial_update:
        Update one or more fields on an existing Transfer.

        permissions: 
            Must have manage_transfer permission.
    update:
        Update a Transfer.

        permissions: 
            Must have manage_transfer permission.
    """
    lookup_field = "id"
    lookup_url_kwarg = "transfer_id"

    permission_classes = [permissions.IsAuthenticated]
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

    filter_backends = (filters.OrderingFilter, filters.SearchFilter)

    ordering_fields = '__all__'
    search_fields = ('id', 'label', 'amount', 'settled')
    filterset_fields = ('id', 'label', 'amount', 'settled')

    def get_queryset(self):
        """
        If user can manage transfers (is runner team member) then they can view and manage all Transfers while authenticated users can only see their transfers and unauthenticated users cannot see anything.
        """
        if self.request.user.has_perm('coin.manage_transfer'):
            return self.get_queryset.all()

        return self.queryset.filter(
            Q(from_user=self.request.user) | Q(to_user=self.request.user)
        )

    def get_permissions(self):
        """
        If the request action is not a read-only request, the user must have the manage_transfer permission.
        """
        if self.action not in ['list', 'retrieve']:
            self.permission_classes = [CanManageTransfer]

        return [permission() for permission in self.permission_classes]
