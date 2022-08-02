from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from org.models import Org

from utils.tests.org import create_org, create_invitation
from utils.tests.user import PASSWORD, create_user

from org.models import Org, OrgInvitation


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
        self.assertEqual(response.data["admin"], org.admin.id)

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

    def test_user_cannot_delete_other_orgs(self):
        org = create_org(self.secondary_user, name="The Best of Times")
        self.assertEqual(Org.objects.count(), 1)
        response = self.client.delete(
            org.get_absolute_url(), HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(response.data.get("id"), None)

    def test_user_can_create_invitation_own_org(self):
        org = create_org(self.user, name="The Best of Times")
        response = self.client.post(
            reverse("org-invitation-list"),
            data={"org": org.id},
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
            reverse("org-invitation-list"), HTTP_AUTHORIZATION=f"Bearer {self.access}"
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
            reverse("org-invitation-list"),
            data={"org": org.id},
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_cannot_list_other_invitations(self):
        org = create_org(self.secondary_user, name="The Best of Times")
        self.assertEqual(OrgInvitation.objects.count(), 0)
        response = self.client.get(
            reverse("org-invitation-list"), HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, [])

    def test_user_cannot_retrieve_other_invitations(self):
        org = create_org(self.secondary_user, name="The Best of Times")
        invitation = create_invitation(org, self.secondary_user)
        response = self.client.get(
            invitation.get_absolute_url(), HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(response.data.get("id"), None)

    def test_user_cannot_update_other_invitations(self):
        org = create_org(self.secondary_user, name="The Best of Times")
        invitation = create_invitation(org, self.secondary_user)
        response = self.client.put(
            invitation.get_absolute_url(),
            data={"expires_at": "2020-01-01T00:00:00Z"},
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(response.data.get("id"), None)

    def test_user_cannot_delete_other_invitations(self):
        org = create_org(self.secondary_user, name="The Best of Times")
        invitation = create_invitation(org, self.secondary_user)
        self.assertEqual(OrgInvitation.objects.count(), 1)
        response = self.client.delete(
            invitation.get_absolute_url(), HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(response.data.get("id"), None)

    def test_user_cannot_create_invitation_for_other_org_with_wrong_token(self):
        org = create_org(self.secondary_user, name="The Best of Times")

        response = self.client.post(
            reverse("org-invitation-list"),
            data={"org": org.id},
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_can_use_invitation(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user)
        response = self.client.post(
            reverse(
                "org-use-invitation",
                kwargs={"org_id": org.id, "org_invitation_id": invitation.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.secondary_access}",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data.get("org"), org.id)
        self.assertEqual(response.data.get("invited_user"), self.secondary_user.id)
        self.assertEqual(response.data.get("invited_by"), self.user.id)
        self.assertEqual(response.data.get("invited_user"), self.secondary_user.id)

    def test_user_cannot_user_invitation_as_member(self):
        org = create_org(self.user, name="The Best of Times")
        invitation = create_invitation(org, self.user)
        response = self.client.post(
            reverse(
                "org-use-invitation",
                kwargs={"org_id": org.id, "org_invitation_id": invitation.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.secondary_access}",
        )
        invitation = create_invitation(org, self.user)
        response = self.client.post(
            reverse(
                "org-use-invitation",
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
                "org-use-invitation",
                kwargs={"org_id": org.id, "org_invitation_id": secondary_invitation.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.secondary_access}",
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            response.data.get("error"), "This invitation is not for this org."
        )

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
                "org-use-invitation",
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