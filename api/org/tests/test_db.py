from django.shortcuts import reverse
from django.test import TestCase

from utils.tests.org import create_org, create_invitation
from utils.tests.user import PASSWORD, create_user

from org.models import OrgRelationship, OrgRole

class OrgTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        response = self.client.post(
            reverse("log_in"),
            data={
                "username": self.user.username,
                "password": PASSWORD,
            },
        )

        # Parse payload data from access token.
        self.access = response.data["access"]

        self.secondary_user = create_user(username="secondaryuser@example.com")
        response = self.client.post(
            reverse("log_in"),
            data={
                "username": self.secondary_user.username,
                "password": PASSWORD,
            },
        )

        # Parse payload data from access token.
        self.secondary_access = response.data["access"]

    def test_user_with_revoked_role_is_revoked(self):
        org = create_org(self.user)
        invitation = create_invitation(org, self.user, role=OrgRole.REVOKED)
        invitation.accept(self.secondary_user)

        relationship = OrgRelationship.objects.get(
            org=org, related_user=self.secondary_user
        )

        self.assertEqual(relationship.role.name, OrgRole.REVOKED)

        # make sure user with revoked role has no permissions at all
        self.assertEqual(relationship.get_all_permissions(), set())

    

    