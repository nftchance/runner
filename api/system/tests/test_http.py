import datetime
import django

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from org.models import Org

from utils.tests.org import create_org, create_invitation
from utils.tests.user import PASSWORD, create_user

from org.models import Org, OrgInvitation
from org.permission_constants import org_permissions
from org.utils import Role, load_permissions

from system.models import Broadcast

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

    def test_cannot_create_broadcast(self):
        response = self.client.post(
            reverse("broadcast-list"),
            data={
                "title": "Test Broadcast",
                "link_text": "Test Link Text",
                "link_url": "http://example.com",
                "external": True,
            },
            HTTP_AUTHORIZATION="Bearer " + self.access,
        )

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_can_list_broadcasts(self):
        response = self.client.get(
            reverse("broadcast-list"), HTTP_AUTHORIZATION="Bearer " + self.access
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # make sure the returned data has all the broadcasts
        self.assertEqual(0, len(response.data))

    def test_can_list_broadcast_after_being_created(self):
        # create broadcast object in db form
        broadcast = Broadcast.objects.create(
            title="Test Broadcast",
            link_text="Test Link Text",
            link_url="http://example.com",
            external=True,
        )

        response = self.client.get(
            reverse("broadcast-list"), HTTP_AUTHORIZATION="Bearer " + self.access
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # make sure the returned data has all the broadcasts
        self.assertEqual(1, len(response.data))
        self.assertEqual(broadcast.title, response.data[0]["title"])
        self.assertEqual(broadcast.link_text, response.data[0]["link_text"])
        self.assertEqual(broadcast.link_url, response.data[0]["link_url"])
        self.assertEqual(broadcast.external, response.data[0]["external"])
                
    def test_broadcast_that_has_expired_is_not_on_list(self):
        # create broadcast object in db form
        broadcast = Broadcast.objects.create(
            title="Test Broadcast",
            link_text="Test Link Text",
            link_url="http://example.com",
            external=True,
            expired_at=django.utils.timezone.now() - datetime.timedelta(days=2)
        )

        response = self.client.get(
            reverse("broadcast-list"), HTTP_AUTHORIZATION="Bearer " + self.access
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # make sure the returned data has all the broadcasts
        self.assertEqual(0, len(response.data))