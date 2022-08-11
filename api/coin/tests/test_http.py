from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from org.models import Org

from utils.tests.org import create_org, create_invitation
from utils.tests.user import PASSWORD, create_user

from org.models import Org, OrgInvitation
from org.permission_constants import org_permissions
from org.utils import Role, load_permissions

from coin.models import Coin, Transfer


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

        load_permissions("org", org_permissions)

        self.coin = Coin.objects.create(name="RUNNER", symbol="RUN")

        self.coin.mint(self.user, 100)
        self.coin.mint(self.secondary_user, 100)

    def test_can_list_transfers(self):
        response = self.client.get(
            reverse("transfer-list"),
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_can_retrieve_transfer(self):
        transfer = Transfer.objects.all().first()
        
        response = self.client.get(
            reverse("transfer-detail", kwargs={"transfer_id": transfer.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], transfer.id)

    def test_cannot_create_transfer(self):
        response = self.client.post(
            reverse("transfer-list"),
            data={
                "from_user": self.user.id,
                "to_user": self.secondary_user.id,
                "amount": 100,
            },
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_update_transfer(self):
        transfer = Transfer.objects.all().first()
        response = self.client.put(
            reverse("transfer-detail", kwargs={"transfer_id": transfer.id}),
            data={
                "from_user": self.user.id,
                "to_user": self.secondary_user.id,
                "amount": 100,
            },
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_delete_transfer(self):
        transfer = Transfer.objects.all().first()
        response = self.client.delete(
            reverse("transfer-detail", kwargs={"transfer_id": transfer.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)