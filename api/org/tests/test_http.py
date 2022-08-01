from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from org.models import Org

from utils.tests.org import create_org
from utils.tests.user import PASSWORD, create_user

from org.models import Org

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
            data={
                "name": "The Best of Times"
            },
            HTTP_AUTHORIZATION=f'Bearer {self.access}'
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
        response = self.client.get(reverse('org-list'),
            HTTP_AUTHORIZATION=f'Bearer {self.access}'
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        exp_org_ids = [str(org.id) for org in orgs]
        act_org_ids = [org.get('id') for org in response.data]
        self.assertCountEqual(exp_org_ids, act_org_ids)

    def test_user_can_retrieve_own_orgs(self):
        org = create_org(self.user, name="The Best of Times")
        response = self.client.get(org.get_absolute_url(),
            HTTP_AUTHORIZATION=f'Bearer {self.access}'
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(str(org.id), response.data.get('id'))

    def test_user_can_update_own_orgs(self):
        org = create_org(self.user, name="The Best of Times")
        response = self.client.put(org.get_absolute_url(),
            data={
                "name": "The Best of Times 2"
            },
            HTTP_AUTHORIZATION=f'Bearer {self.access}'
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data.get('name'), "The Best of Times 2")

    def test_user_can_delete_own_orgs(self):
        org = create_org(self.user, name="The Best of Times")
        self.assertEqual(Org.objects.count(), 1)
        response = self.client.delete(org.get_absolute_url(),
            HTTP_AUTHORIZATION=f'Bearer {self.access}'
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(Org.objects.count(), 0)

    def test_user_cannot_list_other_orgs(self):
        org = create_org(self.secondary_user, name="The Best of Times")
        self.assertEqual(Org.objects.count(), 1)
        response = self.client.get(reverse('org-list'),
            HTTP_AUTHORIZATION=f'Bearer {self.access}'
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, [])

    def test_user_cannot_retrieve_other_orgs(self):
        org = create_org(self.secondary_user, name="The Best of Times")
        self.assertEqual(Org.objects.count(), 1)
        response = self.client.get(org.get_absolute_url(),
            HTTP_AUTHORIZATION=f'Bearer {self.access}'
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(response.data.get('id'), None)

    def test_user_cannot_update_other_orgs(self):
        org = create_org(self.secondary_user, name="The Best of Times")
        self.assertEqual(Org.objects.count(), 1)
        response = self.client.put(org.get_absolute_url(),
            data={
                "name": "The Best of Times 2"
            },
            HTTP_AUTHORIZATION=f'Bearer {self.access}'
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(response.data.get('id'), None)

    def test_user_cannot_delete_other_orgs(self):
        org = create_org(self.secondary_user, name="The Best of Times")
        self.assertEqual(Org.objects.count(), 1)
        response = self.client.delete(org.get_absolute_url(),
            HTTP_AUTHORIZATION=f'Bearer {self.access}'
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(response.data.get('id'), None)