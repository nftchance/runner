import django

from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Proposal
from .serializers import ProposalSerializer

class ProposalViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin, 
    mixins.ListModelMixin, 
    viewsets.GenericViewSet
):
    lookup_field = "id"
    lookup_url_kwarg = "proposal_id"

    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(proposed_by=self.request.user)

    @action(detail=True, methods=['post'])
    def vote(self, request, *args, **kwargs):
        proposal = self.get_object()

        if django.utils.timezone.now() > proposal.closed_at:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                           data={'error': 'Proposal is closed'})

        print('request user balance', request.user.balance)
        if 1 > request.user.balance:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Insufficient balance'})

        if proposal.votes.filter(voter=request.user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Already voted'})

        proposal.vote(request.user, request.data['vote'])
        serializer = ProposalSerializer(proposal)
        return Response(serializer.data)