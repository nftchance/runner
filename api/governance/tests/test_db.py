import datetime

from django.test import TestCase

from utils.tests.user import create_user

from org.permission_constants import org_permissions
from org.utils import load_permissions

from coin.models import Coin
from governance.models import Proposal, ProposalVote
from governance.utils import Vote


class GovernanceTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.secondary_user = create_user(username="secondaryuser@example.com")
        self.tertiary_user = create_user(username="tertiaryuser@example.com")

        load_permissions("org", org_permissions)

        self.coin = Coin.objects.create(name="RUNNER", symbol="RUN")

        self.coin.mint(self.user, 10000000000000)
        self.coin.mint(self.secondary_user, 10000)

    def test_can_create_proposal(self):
        proposal = Proposal.objects.create(
            proposed_by=self.user,
            title="Test Proposal",
            description="This is a test proposal",
            approved=True
        )

        self.assertEqual(proposal.title, "Test Proposal")
        self.assertEqual(proposal.description, "This is a test proposal")

    def test_can_vote(self):
        proposal = Proposal.objects.create(
            proposed_by=self.user,
            title="Test Proposal",
            description="This is a test proposal",
            approved=True
        )

        proposal.vote(self.user, Vote.FOR, 1)

        self.assertEqual(proposal.votes.count(), 1)

    def test_can_vote_and_release_after_closing(self):
        proposal = Proposal.objects.create(
            proposed_by=self.user,
            title="Test Proposal",
            description="This is a test proposal",
            approved=True
        )

        proposal.vote(self.user, Vote.FOR, 1)

        self.user.refresh_from_db()

        self.assertEqual(self.user.balance, 10000000000000 - 1)
        self.assertEqual(proposal.votes.count(), 1)

        proposal.closed_at = "2020-01-01T00:00:00Z"
        proposal.save()

        self.assertEqual(proposal.votes.count(), 1)

        proposal.release_all()

        self.user.refresh_from_db()

        self.assertEqual(f"{self.user.balance}",
                         f"{10000000000000 + 1 * 0.1}000")

    def test_str_is_title(self):
        proposal = Proposal.objects.create(
            proposed_by=self.user,
            title="Test Proposal",
            description="This is a test proposal",
            approved=True
        )

        self.assertEqual(str(proposal), f"[RP{proposal.id}] Test proposal")
