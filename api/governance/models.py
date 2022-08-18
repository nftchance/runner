import datetime
from decimal import Decimal
import django

from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django.contrib.postgres.fields import ArrayField

from coin.models import Coin

from .utils import PROPOSAL_DURATION_DAYS, Vote, Tag


class ProposalVote(models.Model):
    voter = models.ForeignKey('user.User', on_delete=models.CASCADE)

    vote = models.CharField(
        max_length=255, choices=Vote.VOTES, default=Vote.ABSTAIN)
    amount = models.DecimalField(max_digits=20, decimal_places=4, default=0)

    released_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.voter} - {self.vote} - {self.amount}"

    def deposit(self, amount):
        # move the coin into the proposal pool
        coin = Coin.objects.all().first()
        coin.deposit(self.voter, amount)

        self.save()

    def vote_lock_reward(self):
        return self.amount * Decimal(0.1)

    def voter_balance(self):
        return self.amount + self.vote_lock_reward()

    def release(self):
        # move the coin into the voter account
        coin = Coin.objects.all().first()
        coin.withdraw(self.voter, self.voter_balance())

        self.released_at = django.utils.timezone.now()
        self.save()

    class Meta:
        ordering = ['-created_at']


class Proposal(models.Model):
    def save(self, *args, **kwargs):
        if self.tags and not all(tag in dict(Tag.TAGS) for tag in self.tags):
            raise ValueError("One or more tags are invalid")

        if self.approved_at and not self.closed_at:
            self.closed_at = django.utils.timezone.now(
            ) + datetime.timedelta(days=PROPOSAL_DURATION_DAYS)

        if not self.summary:
            self.summary = self.description[:100]

        super(Proposal, self).save(*args, **kwargs)

    proposed_by = models.ForeignKey('user.User', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField()

    summary = models.TextField(blank=True)

    tags = ArrayField(base_field=models.CharField(
        max_length=255, choices=Tag.TAGS), blank=True, null=True)

    votes = models.ManyToManyField(ProposalVote, blank=True)

    approved_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[RP{self.id}] {self.title.lower().capitalize()}"

    def get_absolute_url(self):
        return reverse("proposal-detail", kwargs={"proposal_id": self.pk})

    def approve(self):
        now = django.utils.timezone.now()
        # Prevent users from approving proposals that have an approval date in the past
        if self.approved_at and self.approved_at > now:
            raise ValueError("Proposal already approved")

        if self.closed_at and self.closed_at < now:
            raise ValueError("Proposal already closed")

        self.approved_at = now

        self.save()

    def deny(self):
        now = django.utils.timezone.now()
        if self.closed_at and self.closed_at < now:
            raise ValueError("Proposal already closed")

        self.closed_at = now
        self.save()

    def get_status(self):
        now = django.utils.timezone.now()
        if not self.approved_at or self.approved_at < now:
            return "Pending"

        if now > self.closed_at:
            return "Closed"

        return "In Progress"

    def _get_votes_sum(self, votes):
        return votes.aggregate(Sum('amount'))['amount__sum'] or 0

    def _get_votes(self, vote):
        votes_cache_name = f"_{vote}_votes_cache"
        if not hasattr(self, votes_cache_name):
            setattr(self, votes_cache_name, self.votes.filter(
                vote=vote).aggregate(Sum('amount'))['amount__sum'] or 0)

        return getattr(self, votes_cache_name)

    def get_votes_for(self):
        return self._get_votes(Vote.FOR)

    def get_votes_against(self):
        return self._get_votes(Vote.AGAINST)

    def get_votes_abstain(self):
        return self._get_votes(Vote.ABSTAIN)

    def get_votes_total(self):
        return self._get_votes_sum(self.votes.all())

    def get_vote_percentages(self):
        total = self.get_votes_total() / 100
        if total == 0:
            return {
                Vote.FOR: 0,
                Vote.AGAINST: 0,
                Vote.ABSTAIN: 0
            }

        return {
            Vote.FOR: self.get_votes_for() / total,
            Vote.AGAINST: self.get_votes_against() / total,
            Vote.ABSTAIN: self.get_votes_abstain() / total
        }

    def has_voted(self, voter):
        if voter.is_anonymous:
            return False
        return self.votes.filter(voter=voter).exists()

    def vote(self, voter, _vote, amount):
        now = django.utils.timezone.now()

        if not self.approved_at or self.approved_at > now:
            raise ValueError("Proposal not approved")

        if self.closed_at and self.closed_at < now:
            raise ValueError("Proposal already closed")

        vote_obj = ProposalVote.objects.create(
            voter=voter,
            vote=_vote,
            amount=amount
        )
        vote_obj.deposit(amount)

        self.votes.add(vote_obj)

        self.save()

    def release(self, voter):
        if not self.closed_at:
            raise ValueError("Proposal not closed")

        if self.votes.filter(voter=voter).exists():
            self.votes.filter(voter=voter).first().release()

    def release_all(self):
        if not self.closed_at:
            raise ValueError("Proposal not closed")

        for vote in self.votes.all():
            vote.release()

    class Meta:
        ordering = ['-approved_at', '-closed_at', '-created_at']
        permissions = (
            ("manage_proposal", "Can manage proposal"),
        )
