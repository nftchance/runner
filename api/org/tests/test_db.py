from django.test import TestCase

from utils.tests.org import create_org, create_invitation
from utils.tests.user import create_user

from org.models import OrgRelationship
from org.permission_constants import org_permissions
from org.utils import Role, load_permissions


class OrgTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.secondary_user = create_user(username="secondaryuser@example.com")
        
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
            {'org.view_org', },
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
            {'org.view_org', },
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
            {'org.view_org', 'org.manage_orgrelationship', 'org.manage_orginvitation'}
        )
        self.assertEqual(
            relationship.get_role_permissions(),
            {'org.view_org', 'org.manage_orgrelationship', 'org.manage_orginvitation'}
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
            {'org.view_org', 'org.manage_orgrelationship', 'org.manage_orginvitation', 'org.manage_org'}
        )
        self.assertEqual(
            relationship.get_role_permissions(),
            {'org.view_org', 'org.manage_orgrelationship', 'org.manage_orginvitation', 'org.manage_org'}
        )
        self.assertEqual(
            relationship.get_user_permissions(),
            set()
        )

    def test_user_with_admin_role_has_manage_org_perm(self):
        org = create_org(self.user)
        invitation = create_invitation(org, self.user, role=Role.ADMIN)
        invitation.accept(self.secondary_user)

        relationship = OrgRelationship.objects.get(
            org=org, related_user=self.secondary_user
        )

        self.assertEqual(relationship.role.name, Role.ADMIN)

        # make sure user with admin role has admin permissions
        self.assertEqual(relationship.has_perm('org.manage_org'), True)

    def test_user_with_admin_role_has_manage_org_perms(self):
        org = create_org(self.user)
        invitation = create_invitation(org, self.user, role=Role.ADMIN)
        invitation.accept(self.secondary_user)

        relationship = OrgRelationship.objects.get(
            org=org, related_user=self.secondary_user
        )

        self.assertEqual(relationship.role.name, Role.ADMIN)

        # make sure user with admin role has admin permissions
        self.assertEqual(relationship.has_perms(['org.view_org', 'org.manage_org', 'org.manage_orgrelationship']), True)

    def test_user_with_manager_role_has_revoked_perms_after_being_revoked(self):
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
            {'org.view_org', 'org.manage_orgrelationship', 'org.manage_orginvitation'}
        )
        self.assertEqual(
            relationship.get_role_permissions(),
            {'org.view_org', 'org.manage_orgrelationship', 'org.manage_orginvitation'}
        )
        self.assertEqual(
            relationship.get_user_permissions(),
            set()
        )

        # revoke manager role
        relationship.revoke()

        # have to refresh from database to clear cached permissions
        relationship = OrgRelationship.objects.get(
            org=org, related_user=self.secondary_user
        )

        # make sure user with revoked role has no permissions at all
        self.assertEqual(relationship.get_all_permissions(), set())

    def test_user_with_admin_role_has_revoked_perms_after_being_revoked(self):
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
            {'org.view_org', 'org.manage_orgrelationship', 'org.manage_orginvitation', 'org.manage_org'}
        )
        self.assertEqual(
            relationship.get_role_permissions(),
            {'org.view_org', 'org.manage_orgrelationship', 'org.manage_orginvitation', 'org.manage_org'}
        )
        self.assertEqual(
            relationship.get_user_permissions(),
            set()
        )

        # revoke admin role
        relationship.revoke()

        # have to refresh from database to clear cached permissions
        relationship = OrgRelationship.objects.get(
            org=org, related_user=self.secondary_user
        )

        # make sure user with revoked role has no permissions at all
        self.assertEqual(relationship.get_all_permissions(), set())