import django

from django.db.models import Q

from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from .models import Proposal
from .permissions import CanManageProposal
from .serializers import ProposalSerializer, ProposalVoteSerializer


# TODO: Make sure that pending proposals can only be viewed by the proposer

"""
Non-authenticated users:
- Can see approved proposals

Authenticated users:
- Can see approved proposals + proposals they've submitted

Managing users:
- Can see and manage all proposals
"""
class ProposalViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a Proposal instance.

        permissions: 
            If not approved, must be proposer or have manage_proposal permission. If approved, allow anyone to read.
    list:
        Return all approved proposals + proposals submit by request user.

        permissions: 
            Allow anyone to read. To do anything beyond reading, the requesting user must be the proposer or have manage_proposal permission.
    create:
        Create a new Proposal.

        permissions: 
            To create a proposal there are no locking permissions in place, however the requesting user must have a sufficient balance which acts as a psuedo-permission.
    delete:
        Remove an existing Proposal.

        permissions: 
            If not approved, request user must be proposer or have manage_proposal permission. If approved, request user must have manage_proposal permission.
    partial_update:
        Update one or more fields on an existing Proposal.

        permissions: 
            If not approved, request user must be proposer or have manage_proposal permission. If approved, request user must have manage_proposal permission.
    update:
        Update a Proposal.

        permissions: 
            If not approved, request user must be proposer or have manage_proposal permission. If approved, request user must have manage_proposal permission.

    vote:
        Vote on a Proposal.

        permissions:
            If not approved, request user must be proposer or have manage_proposal permission. If approved, request user must be authenticated. In the processing the balance of the user is required rather than there being an all-permitting permission.
    """
    lookup_field = "id"
    lookup_url_kwarg = "proposal_id"

    permission_classes = [permissions.AllowAny]
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    
    ordering_fields = '__all__'
    search_fields = ('title', 'description')
    filterset_fields = ('id', 'title', 'description', 'approved')

    def get_queryset(self):
        if self.request.user.has_perm('governance.manage_proposal'):
            return super().get_queryset()

        elif self.action == 'retrieve':
            if self.request.user.is_authenticated:
                self.queryset = self.queryset.filter(
                    Q(proposed_by=self.request.user) | Q(approved=True)
                )
            self.queryset = self.queryset.filter(approved=True)

        elif self.action in ['list']:
            # enable filtering list by status
            if self.request.query_params.get('status'):
                status = self.request.query_params.get('status')
                if status == 'in_progress':
                    self.queryset = self.queryset.filter(approved=True)
                elif status == 'pending':
                    self.queryset = self.queryset.filter(approved=False)
                elif status == 'closed':
                    self.queryset = self.queryset.filter(closed_at__lt=django.utils.timezone.now())

            # enable filtering list by tag
            if self.request.query_params.get('tag'):
                tag = self.request.query_params.get('tag')
                self.queryset = self.queryset.filter(tags__contains=[tag,])

        elif self.action in ['partial_update', 'update']:
            self.queryset = self.queryset.filter(proposed_by=self.request.user, approved=False)

        return super().get_queryset()

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, CanManageProposal]
        
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(proposed_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def vote(self, request, *args, **kwargs):
        proposals = Proposal.objects.filter(id=self.kwargs['proposal_id'])

        if not proposals.exists():
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Proposal does not exist"})

        proposal = proposals.first()
        user = request.user

        if not proposal.approved:
            return Response(
                {'error': 'Proposal not approved'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if django.utils.timezone.now() > proposal.closed_at:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'error': 'Proposal is closed'})

        amount = float(request.data.get('amount', 0))

        if request.data['vote'].lower() not in ['for', 'against', 'abstain']:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid vote'})

        if not amount or amount < 1:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'error': 'Amount must be greater than 0'})

        if 1 > user.balance:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Insufficient balance'})

        if proposal.votes.filter(voter=user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Already voted'})

        try:
            obj = proposal.vote(
                user, request.data['vote'].lower(), request.data['amount'])

            serializer = ProposalVoteSerializer(obj)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': str(e)})
 