import datetime
import django

from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse

from .utils import PROPOSAL_DURATION_DAYS, Vote


class ProposalVote(models.Model):
    VOTES = (
        (Vote.FOR, 'For'),
        (Vote.AGAINST, 'Against'),
        (Vote.ABSTAIN, 'Abstain'),
    )

    voter = models.ForeignKey('user.User', on_delete=models.CASCADE)

    vote = models.CharField(
        max_length=255, choices=VOTES, default=Vote.ABSTAIN)
    amount = models.DecimalField(max_digits=20, decimal_places=4, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.proposal} - {self.voter} - {self.vote}'


class Proposal(models.Model):
    def save(self, *args, **kwargs):
        if not self.closed_at:
            self.closed_at = django.utils.timezone.now(
            ) + datetime.timedelta(days=PROPOSAL_DURATION_DAYS)

        super(Proposal, self).save(*args, **kwargs)

    approved = models.BooleanField(default=False)

    proposed_by = models.ForeignKey('user.User', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField()

    votes = models.ManyToManyField(ProposalVote, blank=True, null=True)

    closed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[RP{self.id}] {self.title.lower().capitalize()}"

    def get_absolute_url(self):
        return reverse("proposal-detail", kwargs={"proposal_id": self.pk})

    def get_status(self):
        if django.utils.timezone.now() > self.closed_at:
            return "Closed"

        return "Open"

    def _get_votes_sum(self, votes):
        return votes.aggregate(Sum('amount'))['amount__sum'] or 0

    def _get_votes(self, vote):
        return self._get_votes_sum(self.votes.filter(vote=vote))

    def get_votes_for(self):
        return self._get_votes(Vote.FOR)

    def get_votes_against(self):
        return self._get_votes(Vote.AGAINST)

    def get_votes_abstain(self):
        return self._get_votes(Vote.ABSTAIN)

    def get_votes_total(self):
        return self._get_votes_sum(self.votes.all())

    def vote(self, voter, vote):
        vote = ProposalVote.objects.create(
            voter=voter,
            vote=vote,
            amount=voter.balance
        )

        self.votes.add(vote)

    class Meta:
        ordering = ['-created_at']
