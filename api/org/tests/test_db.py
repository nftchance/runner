from django.shortcuts import reverse
from django.test import TestCase

from utils.tests.org import create_org, create_invitation
from utils.tests.user import PASSWORD, create_user

from org.apps import OrgConfig
from org.models import OrgRelationship, OrgRole
from org.permission_constants import org_permissions
from org.utils import Role, load_permissions


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

        load_permissions("org", org_permissions)

    def test_user_with_revoked_role_is_revoked(self):
        org = create_org(self.user)
        invitation = create_invitation(org, self.user, role=Role.REVOKED)
        invitation.accept(self.secondary_user)

        relationship = OrgRelationship.objects.get(
            org=org, related_user=self.secondary_user
        )

        self.assertEqual(relationship.role.name, Role.REVOKED)

        # make sure user with revoked role has no permissions at all
        self.assertEqual(relationship.get_all_permissions(), set())

    def test_user_with_customer_role_has_customer_permissions(self):
        org = create_org(self.user)
        invitation = create_invitation(org, self.user, role=Role.CUSTOMER)
        invitation.accept(self.secondary_user)

        relationship = OrgRelationship.objects.get(
            org=org, related_user=self.secondary_user
        )

        self.assertEqual(relationship.role.name, Role.CUSTOMER)

        # make sure user with customer role has customer permissions
        self.assertEqual(
            relationship.get_all_permissions(),
            set(),
        )

    def test_user_with_team_role_has_team_permissions(self):
        org = create_org(self.user)
        invitation = create_invitation(org, self.user, role=Role.TEAM)
        invitation.accept(self.secondary_user)

        relationship = OrgRelationship.objects.get(
            org=org, related_user=self.secondary_user
        )

        self.assertEqual(relationship.role.name, Role.TEAM)

        # make sure user with team role has team permissions
        self.assertEqual(
            relationship.get_all_permissions(),
            set(),
        )

    def test_user_with_manager_role_has_manager_permissions(self):
        org = create_org(self.user)
        invitation = create_invitation(org, self.user, role=Role.MANAGER)
        invitation.accept(self.secondary_user)

        relationship = OrgRelationship.objects.get(
            org=org, related_user=self.secondary_user
        )

        self.assertEqual(relationship.role.name, Role.MANAGER)

        # make sure user with manager role has manager permissions
        self.assertEqual(
            relationship.get_all_permissions(),
            {'org.manage_orgrole', 'org.manage_orginvitation'}
        )
        self.assertEqual(
            relationship.get_role_permissions(),
            {'org.manage_orgrole', 'org.manage_orginvitation'}
        )
        self.assertEqual(
            relationship.get_user_permissions(),
            set()
        )

    def test_user_with_admin_role_has_admin_permissions(self):
        org = create_org(self.user)
        invitation = create_invitation(org, self.user, role=Role.ADMIN)
        invitation.accept(self.secondary_user)

        relationship = OrgRelationship.objects.get(
            org=org, related_user=self.secondary_user
        )

        self.assertEqual(relationship.role.name, Role.ADMIN)

        # make sure user with admin role has admin permissions
        self.assertEqual(
            relationship.get_all_permissions(),
            {'org.manage_orgrole', 'org.manage_orginvitation', 'org.manage_org'}
        )
        self.assertEqual(
            relationship.get_role_permissions(),
            {'org.manage_orgrole', 'org.manage_orginvitation', 'org.manage_org'}
        )
        self.assertEqual(
            relationship.get_user_permissions(),
            set()
        )