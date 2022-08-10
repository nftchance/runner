import datetime
from decimal import Decimal
import django

from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse

from coin.models import Coin, Transfer

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
        return f"{self.voter} - {self.vote} - {self.amount}"


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

    def vote(self, voter, _vote, amount):
        vote_obj = ProposalVote.objects.create(
            voter=voter,
            vote=_vote,
            amount=amount
        )
        
        # move the coin into the proposal pool
        coin = Coin.objects.all().first()
        coin.deposit(voter, amount)

        self.votes.add(vote_obj)

        self.save()

    def vote_lock_reward(self, voter):
        if not self.votes.filter(voter=voter).exists():
            return 0

        vote_amount = self.votes.filter(voter=voter).first().amount

        return vote_amount * Decimal(0.1)

    def voter_balance(self, voter):
        return self.votes.filter(voter=voter).first().amount + self.vote_lock_reward(voter)

    def release(self, voter):
        # move the coin into the voter account
        coin = Coin.objects.all().first()
        coin.withdraw(voter, self.voter_balance(voter)) 

    def release_all(self):
        for vote in self.votes.all():
            self.release(vote.voter)

    class Meta:
        ordering = ['-created_at']
