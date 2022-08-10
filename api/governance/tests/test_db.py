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
        )

        self.assertEqual(proposal.title, "Test Proposal")
        self.assertEqual(proposal.description, "This is a test proposal")

    def test_can_vote(self):
        proposal = Proposal.objects.create(
            proposed_by=self.user,
            title="Test Proposal",
            description="This is a test proposal",
        )

        proposal.vote(self.user, Vote.FOR)

        self.assertEqual(proposal.votes.count(), 1)

    def test_str_is_title(self):
        proposal = Proposal.objects.create(
            proposed_by=self.user,
            title="Test Proposal",
            description="This is a test proposal",
        )

        self.assertEqual(str(proposal), f"[RP{proposal.id}] Test proposal")