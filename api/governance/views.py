import django

from rest_framework import mixins, permissions, status, views, viewsets, filters, generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Proposal
from .serializers import ProposalSerializer, ProposalVoteSerializer


class ProposalVoteView(views.APIView):
    def post(self, request, *args, **kwargs):
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
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    
    ordering_fields = '__all__'
    search_fields = ('title', 'description')
    filterset_fields = ('id', 'title', 'description', 'approved')

    def perform_create(self, serializer):
        serializer.save(proposed_by=self.request.user)
