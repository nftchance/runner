import datetime
import django

from django.db import models

from .utils import PROPOSAL_SUBMISSION_BALANCE_MINIMUM, PROPOSAL_DURATION_DAYS, Vote

class ProposalVote(models.Model):
    """
    A vote on a proposal.
    """
    VOTES = (
        (Vote.FOR, 'For'),
        (Vote.AGAINST, 'Against'),
        (Vote.ABSTAIN, 'Abstain'),
    )

    voter = models.ForeignKey('user.User', on_delete=models.CASCADE)

    vote = models.CharField(max_length=255, choices=VOTES, default=Vote.ABSTAIN)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.proposal} - {self.voter} - {self.vote}'

class Proposal(models.Model):
    def save(self, *args, **kwargs):
        if not self.proposed_by.is_superuser and self.proposed_by.balance < PROPOSAL_SUBMISSION_BALANCE_MINIMUM:
            raise ValueError("Insufficient balance")

        if not self.closed_at:
            self.closed_at = django.utils.timezone.now() + datetime.timedelta(days=PROPOSAL_DURATION_DAYS)

        super(Proposal, self).save(*args, **kwargs)

    proposed_by = models.ForeignKey('user.User', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField()

    votes = models.ManyToManyField(ProposalVote)

    closed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[RP{self.id}] {self.title.lower().capitalize()}"

    def vote(self, voter, vote):
        if django.utils.timezone.now() > self.closed_at:
            raise ValueError("Proposal already closed")

        if 1 > voter.balance:
            raise ValueError("Insufficient balance")

        if self.votes.filter(voter=voter).exists():
            raise ValueError("Already voted")

        vote = ProposalVote.objects.create(
            voter=voter,
            vote=vote
        )

        self.votes.add(vote)

    class Meta:
        ordering = ['-created_at']