import django

from rest_framework import serializers

from .models import Proposal, ProposalVote
from .utils import PROPOSAL_SUBMISSION_BALANCE_MINIMUM


class ProposalVoteSerializer(serializers.Serializer):
    class Meta:
        model = ProposalVote
        fields = ('id', 'voter', 'vote', 'created_at')
        extra_kwargs = {
            'id': {'read_only': True},
            'voter': {'read_only': True},
            'vote': {'read_only': True},
            'created_at': {'read_only': True},
        }


class ProposalSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    votes_for = serializers.SerializerMethodField()
    votes_against = serializers.SerializerMethodField()
    votes_abstain = serializers.SerializerMethodField()
    votes_total = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.get_status()

    def get_votes_for(self, obj):
        return obj.get_votes_for()

    def get_votes_against(self, obj):
        return obj.get_votes_against()

    def get_votes_abstain(self, obj):
        return obj.get_votes_abstain()

    def get_votes_total(self, obj):
        return obj.get_votes_total()

    def create(self, *args, **kwargs):
        if self.context['request'].user.balance < PROPOSAL_SUBMISSION_BALANCE_MINIMUM:
            raise serializers.ValidationError(
                {'error': 'Insufficient balance'})

        return super(ProposalSerializer, self).create(*args, **kwargs)

    class Meta:
        model = Proposal
        fields = '__all__'
        extra_kwargs = {
            'proposed_by': {'read_only': True},
            'votes': {'read_only': True},
            'closed_at': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
