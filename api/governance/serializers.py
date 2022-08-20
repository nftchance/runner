import django

from rest_framework import serializers

from user.serializers import UserSerializer

from .models import Proposal, ProposalVote
from .utils import PROPOSAL_SUBMISSION_BALANCE_MINIMUM, Tag


class ProposalVoteSerializer(serializers.ModelSerializer):
    voter = UserSerializer(read_only=True)
    
    def validate_vote(self, value):
        if value not in ['for', 'against', 'abstain']:
            raise serializers.ValidationError('Invalid vote')
        return value

    def create(self, validated_data):
        # make sure amount is less than the user balance
        user = self.context['request'].user
        amount = validated_data['amount']
        if amount > user.balance:
            raise serializers.ValidationError('Insufficient balance')

    class Meta:
        model = ProposalVote
        fields = "__all__"
        extra_kwargs = {
            'id': {'read_only': True},
            'voter': {'read_only': True},
            'vote': {'read_only': True},
            'amount': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

class ProposalSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(
        max_length=256), allow_empty=True, required=False)

    status = serializers.SerializerMethodField()

    votes_for = serializers.SerializerMethodField()
    votes_against = serializers.SerializerMethodField()
    votes_abstain = serializers.SerializerMethodField()
    votes_total = serializers.SerializerMethodField()
    vote_percentages = serializers.SerializerMethodField()

    proposed_by = UserSerializer(read_only=True)

    votes = ProposalVoteSerializer(many=True, read_only=True)

    has_voted = serializers.SerializerMethodField()

    def validate_amount(self, value):
        if not value or value < 1:
            raise serializers.ValidationError(
                {'error': 'Amount must be greater than 0'})

        return value


    def validate_tags(self, value):
        if not all(tag in dict(Tag.TAGS) for tag in value):
            raise serializers.ValidationError(
                {'error': 'Invalid tags'})

        return value

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

    def get_vote_percentages(self, obj):
        return obj.get_vote_percentages()

    def get_has_voted(self, obj):
        if 'request' not in self.context:
            return False

        return obj.has_voted(self.context['request'].user)

    def create(self, *args, **kwargs):
        if self.context['request'].user.balance < PROPOSAL_SUBMISSION_BALANCE_MINIMUM:
            raise serializers.ValidationError(
                {'error': 'Insufficient balance'})

        if 'tags' in self.validated_data and not all(tag in dict(Tag.TAGS) for tag in self.validated_data['tags']):
            raise serializers.ValidationError(
                {'error': 'Invalid tags'})

        return super(ProposalSerializer, self).create(*args, **kwargs)

    class Meta:
        model = Proposal
        fields = '__all__'
        extra_kwargs = {
            'proposed_by': {'read_only': True},
            'votes': {'read_only': True},
            'approved_at': {'read_only': True},
            'closed_at': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
