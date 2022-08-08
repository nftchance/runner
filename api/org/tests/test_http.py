from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from org.models import Org

from utils.tests.org import create_org, create_invitation
from utils.tests.user import PASSWORD, create_user

from org.models import Org, OrgInvitation
from org.permission_constants import org_permissions
from org.utils import Role, load_permissions


class HttpTest(APITestCase):
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

    """
    Tests for top level organization management.
    """
    def test_user_can_create_org(self):
        response = self.client.post(
            reverse("org-list"),
            data={"name": "The Best of Times"},
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        org = Org.objects.get(name="The Best of Times")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data["id"], org.id)
        self.assertEqual(response.data["name"], org.name)

    def test_user_can_list_own_orgs(self):
        orgs = [
            create_org(self.user, name="The Best of Times"),
            create_org(self.user, name="The Worst of Times"),
        ]
        response = self.client.get(
            reverse("org-list"), HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        exp_org_ids = [str(org.id) for org in orgs]
        act_org_ids = [org.get("id") for org in response.data]
        self.assertCountEqual(exp_org_ids, act_org_ids)

    def test_user_can_retrieve_own_orgs(self):
        org = create_org(self.user, name="The Best of Times")
        response = self.client.get(
            org.get_absolute_url(), HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(str(org.id), response.data.get("id"))

    def test_user_can_update_own_orgs(self):
        org = create_org(self.user, name="The Best of Times")
        response = self.client.put(
            org.get_absolute_url(),
            data={"name": "The Best of Times 2"},
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data.get("name"), "The Best of Times 2")

    def test_user_can_delete_own_orgs(self):
        org = create_org(self.user, name="The Best of Times")
        self.assertEqual(Org.objects.count(), 1)
        response = self.client.delete(
            org.get_absolute_url(), HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(Org.objects.count(), 0)

    def test_user_cannot_list_other_orgs(self):
        org = create_org(self.secondary_user, name="The Best of Times")
        self.assertEqual(Org.objects.count(), 1)
        response = self.client.get(
            reverse("org-list"), HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, [])

    def test_user_cannot_retrieve_other_orgs(self):
        org = create_org(self.secondary_user, name="The Best of Times")
        self.assertEqual(Org.objects.count(), 1)
        response = self.client.get(
            org.get_absolute_url(), HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(response.data.get("id"), None)

    def test_user_cannot_update_other_orgs(self):
        org = create_org(self.secondary_user, name="The Best of Times")
        self.assertEqual(Org.objects.count(), 1)
        response = self.client.put(
            org.get_absolute_url(),
            data={"name": "The Best of Times 2"},
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(response.data.get("id"), None)
 
    """
    A POST request creates a resource. The server assigns a URI for the new resource and returns that URI to the client. In the REST model, you frequently apply POST requests to collections. The new resource is added to the collection. A POST request can also be used to submit data for processing to an existing resource, without any new resource being created.

    A PUT request creates a resource or updates an existing resource. The client specifies the URI for the resource. The request body contains a complete representation of the resource. If a resource with this URI already exists, it is replaced. Otherwise, a new resource is created, if the server supports doing so. PUT requests are most frequently applied to resources that are individual items, such as a specific customer, rather than collections. A server might support updates but not creation via PUT. Whether to support creation via PUT depends on whether the client can meaningfully assign a URI to a resource before it exists. If not, then use POST to create resources and PUT or PATCH to update.

    A PATCH request performs a partial update to an existing resource. The client specifies the URI for the resource. The request body specifies a set of changes to apply to the resource. This can be more efficient than using PUT, because the client only sends the changes, not the entire representation of the resource. Technically PATCH can also create a new resource (by specifying a set of updates to a "null" resource), if the server supports this.
    """

    def test_user_cannot_delete_other_orgs(self):
        org = create_org(self.secondary_user, name="The Best of Times")
        self.assertEqual(Org.objects.count(), 1)
        response = self.client.delete(
            org.get_absolute_url(), HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(response.data.get("id"), None)

    def test_user_cannot_update_id_of_own_org_post(self):
        org = create_org(self.user, name="The Best of Times")
        self.assertEqual(Org.objects.count(), 1)
        response = self.client.post(
            org.get_absolute_url(),
            data={"id": "123"},
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
        self.assertEqual(Org.objects.all().count(), 1)

    def test_user_cannot_update_id_of_own_org_put(self):
        org = create_org(self.user, name="The Best of Times")
        self.assertEqual(Org.objects.count(), 1)
        response = self.client.put(
            reverse("org-detail", kwargs={"org_id": org.id}),
            data={
                "name": "The Best of Times 2",
            },
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        print([obj.name for obj in Org.objects.all()])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(Org.objects.all().count(), 1)
 
    def test_user_can_update_name_of_org_patch(self):
        org = create_org(self.user, name="The Best of Times")
        self.assertEqual(Org.objects.count(), 1)
        response = self.client.patch(
            org.get_absolute_url(),
            data={"name": "The Best of Times 2"},
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            format="json"
        )
        self.assertEqual(response.request['REQUEST_METHOD'], 'PATCH')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data.get("name"), "The Best of Times 2")
        self.assertEqual(Org.objects.all().count(), 1)

    # def test_user_cannot_update_id_of_own_org_patch(self):
    #     org = create_org(self.user, name="The Best of Times")
    #     self.assertEqual(Org.objects.count(), 1)
    #     response = self.client.patch(
    #         org.get_absolute_url(),
    #         data={"id": "123"},
    #         HTTP_AUTHORIZATION=f"Bearer {self.access}",
    #     )
    #     self.assertEqual(Org.objects.all().count(), 1)
    #     self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    # def test_user_cannot_update_created_at_of_own_org(self):
    #     org = create_org(self.user, name="The Best of Times")
    #     # send request with ignored updated_at field to serializer
    #     response = self.client.patch(
    #         org.get_absolute_url(),
    #         data={"created_at": "2020-01-01T00:00:00Z"},
    #         HTTP_AUTHORIZATION=f"Bearer {self.access}",
    #     )
    #     # confirm that updated_at field is not updated
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     self.assertEqual(response.data.get("name"), "The Best of Times")
    #     self.assertEqual(Org.objects.all().count(), 1)
    #     self.assertEqual(response.data.get("created_at"), f'{org.created_at}')

    """
    Tests for organization invitation management.
    """
    def test_user_can_create_invitation_own_org(self):
        org = create_org(self.user, name="The Best of Times")
        response = self.client.post(
            reverse("org-invitation-list", kwargs={"org_id": org.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )

        invitation = OrgInvitation.objects.first()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data["id"], invitation.id)

    def test_user_can_list_own_invitations(self):
        org = create_org(self.user, name="The Best of Times")

        invitations = [
            create_invitation(org, self.user),
            create_invitation(org, self.user),
        ]

        response = self.client.get(
            reverse("org-invitation-list", kwargs={"org_id": org.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        exp_inv_ids = [str(invitation.id) for invitation in invitations]
        act_inv_ids = [invitation.get("id") for invitation in response.data]
        self.assertCountEqual(exp_inv_ids, act_inv_ids)

    def test_user_can_retrieve_own_invitations(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user)
        response = self.client.get(
            invitation.get_absolute_url(), HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(str(invitation.id), response.data.get("id"))

    def test_user_can_update_own_invitations(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user)
        response = self.client.put(
            invitation.get_absolute_url(),
            data={"expires_at": "2020-01-01T00:00:00Z"},
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data.get("expires_at"), "2020-01-01T00:00:00Z")

    def test_user_can_delete_own_invitations(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user)
        self.assertEqual(OrgInvitation.objects.count(), 1)
        response = self.client.delete(
            invitation.get_absolute_url(), HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(OrgInvitation.objects.count(), 0)

    def test_user_cannot_create_invitation_for_other_org(self):
        org = create_org(self.secondary_user, name="The Best of Times")

        response = self.client.post(
            reverse("org-invitation-list", kwargs={"org_id": org.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_cannot_list_other_invitations(self):
        org = create_org(self.secondary_user, name="The Best of Times")
        self.assertEqual(OrgInvitation.objects.count(), 0)
        response = self.client.get(
            reverse("org-invitation-list", kwargs={"org_id": org.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_cannot_retrieve_other_invitations(self):
        org = create_org(self.secondary_user, name="The Best of Times")
        invitation = create_invitation(org, self.secondary_user)
        response = self.client.get(
            invitation.get_absolute_url(), HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_cannot_update_other_invitations(self):
        org = create_org(self.secondary_user, name="The Best of Times")
        invitation = create_invitation(org, self.secondary_user)
        response = self.client.put(
            invitation.get_absolute_url(),
            data={"expires_at": "2020-01-01T00:00:00Z"},
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_cannot_delete_other_invitations(self):
        org = create_org(self.secondary_user, name="The Best of Times")
        invitation = create_invitation(org, self.secondary_user)
        self.assertEqual(OrgInvitation.objects.count(), 1)
        response = self.client.delete(
            invitation.get_absolute_url(), HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_cannot_create_invitation_for_other_org_with_wrong_token(self):
        org = create_org(self.secondary_user, name="The Best of Times")

        response = self.client.post(
            reverse("org-invitation-list", kwargs={'org_id': org.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_can_use_invitation_customer(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user)
        response = self.client.post(
            reverse(
                "org-invitation-accept",
                kwargs={"org_id": org.id, "org_invitation_id": invitation.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.secondary_access}",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data.get("org"), org.id)
        self.assertEqual(response.data.get("invited_user"), self.secondary_user.id)
        self.assertEqual(response.data.get("invited_by"), self.user.id)
        self.assertEqual(response.data.get("invited_user"), self.secondary_user.id)
        self.assertEqual(response.data.get("role"), "customer")

    def test_user_can_use_invitation_team(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user, role="team")
        response = self.client.post(
            reverse(
                "org-invitation-accept",
                kwargs={"org_id": org.id, "org_invitation_id": invitation.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.secondary_access}",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data.get("org"), org.id)
        self.assertEqual(response.data.get("invited_user"), self.secondary_user.id)
        self.assertEqual(response.data.get("invited_by"), self.user.id)
        self.assertEqual(response.data.get("invited_user"), self.secondary_user.id)
        self.assertEqual(response.data.get("role"), "team")

    def test_user_can_use_invitation_manager(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user, role="manager")
        response = self.client.post(
            reverse(
                "org-invitation-accept",
                kwargs={"org_id": org.id, "org_invitation_id": invitation.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.secondary_access}",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data.get("org"), org.id)
        self.assertEqual(response.data.get("invited_user"), self.secondary_user.id)
        self.assertEqual(response.data.get("invited_by"), self.user.id)
        self.assertEqual(response.data.get("invited_user"), self.secondary_user.id)
        self.assertEqual(response.data.get("role"), "manager")

    def test_user_can_use_invitation_admin(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user, role="admin")
        response = self.client.post(
            reverse(
                "org-invitation-accept",
                kwargs={"org_id": org.id, "org_invitation_id": invitation.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.secondary_access}",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data.get("org"), org.id)
        self.assertEqual(response.data.get("invited_user"), self.secondary_user.id)
        self.assertEqual(response.data.get("invited_by"), self.user.id)
        self.assertEqual(response.data.get("invited_user"), self.secondary_user.id)
        self.assertEqual(response.data.get("role"), "admin")

    def test_user_cannot_user_invitation_as_member(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user)
        response = self.client.post(
            reverse(
                "org-invitation-accept",
                kwargs={"org_id": org.id, "org_invitation_id": invitation.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.secondary_access}",
        )
        invitation = create_invitation(org, self.user)
        response = self.client.post(
            reverse(
                "org-invitation-accept",
                kwargs={"org_id": org.id, "org_invitation_id": invitation.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.secondary_access}",
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(
            response.data.get("error"), "You are already a member of this org."
        )

    def test_user_cannot_use_invitation_for_other_org(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user)
        secondary_org = create_org(self.secondary_user, name="The Worst of Times")
        secondary_invitation = create_invitation(secondary_org, self.secondary_user)

        response = self.client.post(
            reverse(
                "org-invitation-accept",
                kwargs={"org_id": org.id, "org_invitation_id": secondary_invitation.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.secondary_access}",
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_user_cannot_use_invitation_twice(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user)
        invitation.accept(self.secondary_user)

        # create another user
        self.tertiary_user = create_user(username="tertiaryser@example.com")
        user_response = self.client.post(
            reverse("log_in"),
            data={
                "username": self.tertiary_user.username,
                "password": PASSWORD,
            },
        )
        self.tertiary_access = user_response.data["access"]

        response = self.client.post(
            reverse(
                "org-invitation-accept",
                kwargs={"org_id": org.id, "org_invitation_id": invitation.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.tertiary_access}",
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code
        )
        self.assertEqual(
            response.data.get("error"),
            "This invitation has already been used.",
        )

    def test_user_can_revoke_invitation_of_own_org(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user)

        # accept invitation
        invitation.accept(self.secondary_user)

        # revoke invitation
        response = self.client.post(
            reverse(
                "org-invitation-revoke",
                kwargs={"org_id": org.id, "org_invitation_id": invitation.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual(response.data.get('invited_by'), None)
        self.assertNotEqual(response.data.get('revoked_at'), None)

    def test_user_cannot_revoke_invitation_of_other_org(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user)

        # accept invitation
        invitation.accept(self.secondary_user)

        # revoke invitation
        response = self.client.post(
            reverse(
                "org-invitation-revoke",
                kwargs={"org_id": org.id, "org_invitation_id": invitation.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.secondary_access}",
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_cannot_revoke_invitation_from_organization_with_wrong_invitation_id(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user)

        # accept invitation
        invitation.accept(self.secondary_user)

        # revoke invitation
        response = self.client.post(
            reverse(
                "org-invitation-revoke",
                kwargs={"org_id": org.id, "org_invitation_id": 'CA9',}
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_user_cannot_revoke_invitation_of_wrong_organization(self):
        org = create_org(self.user, name="The Best of Times")
        secondary_org = create_org(self.secondary_user, name="The Worst of Times")
        invitation = create_invitation(secondary_org, self.user)

        # accept invitation
        invitation.accept(self.secondary_user)

        # revoke invitation
        response = self.client.post(
            reverse(
                "org-invitation-revoke",
                kwargs={"org_id": org.id, "org_invitation_id": invitation.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_user_cannot_revoke_invitation_twice(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user)

        # accept invitation
        invitation.accept(self.secondary_user)
        invitation.revoke()

        response = self.client.post(
            reverse(
                "org-invitation-revoke",
                kwargs={"org_id": org.id, "org_invitation_id": invitation.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            response.data.get("error"), "This invitation has already been revoked."
        )
    
    """
    Tests for organization relationships of the users within this organization.
    """
    def test_admin_can_list_own_orgs_relationships(self):
        org = create_org(self.user, name="The Best of Times")

        relationship_obj = self.user.org_relationships.get(org=org)

        response = self.client.get(
            reverse(
                "org-relationship-list",
                kwargs={"org_id": org.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            relationship_obj.id, response.data[0].get("id"), 
        )

    # def test_admin_cannot_create_relationship_directly(self):
    #     org = create_org(self.user, name="The Best of Times")

    #     response = self.client.post(
    #         reverse(
    #             "org-relationship-list",
    #             kwargs={"org_id": org.id},
    #         ),
    #         data={'org': org.id, 'related_user': self.secondary_user},
    #         HTTP_AUTHORIZATION=f"Bearer {self.access}",
    #     )

    #     self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    # def test_user_cannot_update_id_of_own_relationship(self):
    #     org = create_org(self.user, name="The Best of Times")
    #     relationship_obj = self.user.org_relationships.get(org=org)

    #     self.assertEqual(Org.objects.count(), 1)
    #     response = self.client.put(
    #         relationship_obj.get_absolute_url(),
    #         data={"id": "123"},
    #         HTTP_AUTHORIZATION=f"Bearer {self.access}",
    #     )
    #     self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        # self.assertEqual(response.data.get("id"), None)

    # def test_admin_cannot_update_readonly_field_of_relationship(self):
    #     org = create_org(self.user, name="The Best of Times")

    #     relationship_obj = self.user.org_relationships.get(org=org)

    #     response = self.client.patch(
    #         reverse(
    #             "org-relationship-detail",
    #             kwargs={"org_id": org.id, "org_relationship_id": relationship_obj.id},
    #         ),
    #         data={'id': '123'},
    #         HTTP_AUTHORIZATION=f"Bearer {self.access}",
    #     )

    #     self.assertEqual(response.data['id'], org.id)
        # self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_user_with_customer_role_cannot_list_org_relationships_even_as_customer(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user, role=Role.CUSTOMER)

        # accept invitation
        invitation.accept(self.secondary_user)

        response = self.client.get(
            reverse(
                "org-relationship-list",
                kwargs={"org_id": org.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.secondary_access}",
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_with_team_role_cannot_list_org_relationships_even_as_team(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user, role=Role.TEAM)

        # accept invitation
        invitation.accept(self.secondary_user)

        response = self.client.get(
            reverse(
                "org-relationship-list",
                kwargs={"org_id": org.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.secondary_access}",
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_revoked_user_cannot_view_relationships(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user)

        # accept invitation
        invitation.accept(self.secondary_user)
        invitation.revoke()

        relationship_obj = self.secondary_user.org_relationships.get(org=org)

        response = self.client.get(
            reverse(
                "org-relationship-detail",
                kwargs={"org_id": org.id, "org_relationship_id": relationship_obj.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.secondary_access}",
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)