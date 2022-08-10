import datetime
import django

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from utils.tests.user import PASSWORD, create_user

from coin.models import Coin

from org.models import Org
from org.permission_constants import org_permissions
from org.utils import load_permissions

from governance.models import Proposal, ProposalVote
from governance.utils import Vote


class HttpTest(APITestCase):
    def setUp(self):
        self.user = create_user()
        response = self.client.post(
            reverse("log-in"),
            data={
                "username": self.user.username,
                "password": PASSWORD,
            },
        )

        # Parse payload data from access token.
        self.access = response.data["access"]

        self.secondary_user = create_user(username="secondaryuser@example.com")
        response = self.client.post(
            reverse("log-in"),
            data={
                "username": self.secondary_user.username,
                "password": PASSWORD,
            },
        )

        # Parse payload data from access token.
        self.secondary_access = response.data["access"]

        self.tertiary_user = create_user(username="tertiaryuser@example.com")
        response = self.client.post(
            reverse("log-in"),
            data={
                "username": self.tertiary_user.username,
                "password": PASSWORD,
            },
        )

        # Parse payload data from access token.
        self.tertiary_access = response.data["access"]

        load_permissions("org", org_permissions)

        self.coin = Coin.objects.create(name="RUNNER", symbol="RUN")

        self.coin.mint(self.user, 10000000000000)
        self.coin.mint(self.secondary_user, 10000)

    def test_can_create_proposal(self):
        response = self.client.post(
            reverse("proposal-list"),
            data={
                "title": "Test Proposal",
                "description": "Test proposal",
                "proposed_by": self.user.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        proposal = Proposal.objects.get(title="Test Proposal")

        self.assertEqual(response.data.get('id'), proposal.id)

        self.assertEqual(response.data["description"], proposal.description)
        self.assertEqual(response.data["status"], proposal.get_status())
        self.assertEqual(response.data["votes_for"], 0)
        self.assertEqual(response.data["votes_against"], 0)
        self.assertEqual(response.data["votes_abstain"], 0)
        self.assertEqual(response.data["votes_total"], 0)

    def test_can_list_proposals(self):
        proposals = [
            Proposal.objects.create(
                title="Test Proposal",
                description="Test proposal",
                proposed_by=self.user,
                approved=True
            ),
            Proposal.objects.create(
                title="Secondary Proposal",
                description="Secondary proposal",
                proposed_by=self.user,
                approved=True
            )
        ]

        response = self.client.get(
            reverse("proposal-list"),
            HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        exp_proposal_ids = [proposal.id for proposal in proposals]
        act_proposal_ids = [proposal.get("id") for proposal in response.data]
        self.assertCountEqual(exp_proposal_ids, act_proposal_ids)

    def test_can_retrieve_proposal(self):
        proposal = Proposal.objects.create(
            title="Test Proposal",
            description="Test proposal",
            proposed_by=self.user,
            approved=True
        )

        response = self.client.get(
            reverse("proposal-detail", kwargs={"proposal_id": proposal.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["id"], proposal.id)

    def test_cannot_create_proposal_with_insufficient_balance(self):
        response = self.client.post(
            reverse("proposal-list"),
            data={
                "title": "Test Proposal",
                "description": "Test proposal",
            },
            HTTP_AUTHORIZATION=f"Bearer {self.secondary_access}"
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(f"{response.data['error']}", "Insufficient balance")

    def test_can_vote(self):
        proposal = Proposal.objects.create(
            title="Test Proposal",
            description="Test proposal",
            proposed_by=self.secondary_user,
            approved=True
        )

        response = self.client.post(
            reverse("proposal-vote", kwargs={"proposal_id": proposal.id}),
            data={
                "vote": Vote.FOR,
            },
            HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        proposal = Proposal.objects.get(id=proposal.id)

        self.assertEqual(proposal.votes.count(), 1)
        self.assertEqual(response.data["votes_for"], self.user.balance)
        self.assertEqual(response.data["votes_against"], 0)
        self.assertEqual(response.data["votes_abstain"], 0)
        self.assertEqual(response.data["votes_total"], self.user.balance)

    def test_cannot_vote_after_proposal_closed(self):
        proposal = Proposal.objects.create(
            title="Test Proposal",
            description="Test proposal",
            proposed_by=self.user,
            approved=True,
            closed_at=django.utils.timezone.now() - datetime.timedelta(days=1),
        )

        response = self.client.post(
            reverse("proposal-vote", kwargs={"proposal_id": proposal.id}),
            data={
                "vote": Vote.FOR,
            },
            HTTP_AUTHORIZATION=f"Bearer {self.secondary_access}"
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(f"{response.data['error']}", "Proposal is closed")

    def test_cannot_vote_twice_on_same_proposal(self):
        proposal = Proposal.objects.create(
            title="Test Proposal",
            description="Test proposal",
            proposed_by=self.secondary_user,
            approved=True,
        )

        response = self.client.post(
            reverse("proposal-vote", kwargs={"proposal_id": proposal.id}),
            data={
                "vote": Vote.FOR,
            },
            HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response = self.client.post(
            reverse("proposal-vote", kwargs={"proposal_id": proposal.id}),
            data={
                "vote": Vote.FOR,
            },
            HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(f"{response.data['error']}", "Already voted")

    def test_cannot_vote_with_insufficient_balance(self):
        proposal = Proposal.objects.create(
            title="Test Proposal",
            description="Test proposal",
            proposed_by=self.user,
            approved=True,
        )

        response = self.client.post(
            reverse("proposal-vote", kwargs={"proposal_id": proposal.id}),
            data={
                "vote": Vote.FOR,
            },
            HTTP_AUTHORIZATION=f"Bearer {self.tertiary_access}"
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(f"{response.data['error']}", "Insufficient balance")

    def test_cannot_vote_on_nonexistent_proposal(self):
        response = self.client.post(
            reverse("proposal-vote", kwargs={"proposal_id": 1}),
            data={
                "vote": Vote.FOR,
            },
            HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_cannot_update_proposal(self):
        proposal = Proposal.objects.create(
            title="Test Proposal",
            description="Test proposal",
            proposed_by=self.user,
            approved=True
        )

        response = self.client.put(
            reverse("proposal-detail", kwargs={"proposal_id": proposal.id}),
            data={
                "title": "Updated Title",
                "description": "Updated description",
            },
            HTTP_AUTHORIZATION=f"Bearer {self.secondary_access}"
        )

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)


    def test_cannot_vote_on_proposal_not_approved(self):
        proposal = Proposal.objects.create(
            title="Test Proposal",
            description="Test proposal",
            proposed_by=self.secondary_user,
        )

        response = self.client.post(
            reverse("proposal-vote", kwargs={"proposal_id": proposal.id}),
            data={
                "vote": Vote.FOR,
            },
            HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(f"{response.data['error']}", "Proposal not approved")