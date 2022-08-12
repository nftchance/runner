import datetime
import django
from ..models import WaitlistEntry

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

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED,
                         response.status_code)

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

    def test_can_create_waitlist_entry(self):
        response = self.client.post(
            reverse("waitlist-list"),
            data={
                "email": "user@example.com"
            }
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_cannot_create_waitlist_entry_for_same_email_address(self):
        response = self.client.post(
            reverse("waitlist-list"),
            data={
                "email": "user@example.com"
            }
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        response = self.client.post(
            reverse("waitlist-list"),
            data={
                "email": "user@example.com"
            }
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            response.data['email'][0],
            'waitlist entry with this email already exists.')

    def test_cannot_create_waitlist_entry_with_salted_email_address(self):
        response = self.client.post(
            reverse("waitlist-list"),
            data={
                "email": "user@example.com"
            }
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        response = self.client.post(
            reverse("waitlist-list"),
            data={
                "email": "user+test@example.com"
            }
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            response.data['email'][0],
            'Waitlist entry with email already exists.')

    def test_can_accept_waitlist_invite(self):
        response = self.client.post(
            reverse("waitlist-list"),
            data={
                "email": "user@example.com"
            }
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        waitlist = WaitlistEntry.objects.get(pk=response.data['id'])
        waitlist.invite()

        response = self.client.post(
            reverse("waitlist-accept",
                    kwargs={'waitlist_entry_id': waitlist.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_cannot_accept_invitation_twice(self):
        response = self.client.post(
            reverse("waitlist-list"),
            data={
                "email": "user@example.com"
            }
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        waitlist = WaitlistEntry.objects.get(pk=response.data['id'])
        waitlist.invite()

        response = self.client.post(
            reverse("waitlist-accept",
                    kwargs={'waitlist_entry_id': waitlist.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response = self.client.post(
            reverse("waitlist-accept",
                    kwargs={'waitlist_entry_id': waitlist.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_user_cannot_accept_invitation_for_different_email(self):
        response = self.client.post(
            reverse("waitlist-list"),
            data={
                "email": "user@example.com"
            }
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        waitlist = WaitlistEntry.objects.get(pk=response.data['id'])
        waitlist.invite()

        response = self.client.post(
            reverse("waitlist-accept",
                    kwargs={'waitlist_entry_id': waitlist.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.secondary_access}"
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_user_cannot_accept_invitation_exceeding_daily_limit(self):
        # create five waitlist entries
        for i in range(5):
            username = f"user{i}@example.com"

            response = self.client.post(
                reverse("waitlist-list"),
                data={
                    "email": username,
                }
            )

            obj = WaitlistEntry.objects.get(pk=response.data['id'])

            obj.invite()

            self.assertEqual(status.HTTP_201_CREATED, response.status_code)

            user = create_user(username=username)

            # log into user
            user_response = self.client.post(
                reverse("log-in"),
                data={
                    "username": self.secondary_user.username,
                    "password": PASSWORD,
                },
            )

            # accept waitlist entry
            entry = WaitlistEntry.objects.get(email=username)

            self.assertEqual(entry.time_until_can_accept(), 0)

            response = self.client.post(
                reverse("waitlist-accept",
                        kwargs={'waitlist_entry_id': entry.id}),
                HTTP_AUTHORIZATION=f"Bearer {user_response.data['access']}"
            )

        # create another waitlist entry
        response = self.client.post(
            reverse("waitlist-list"),
            data={
                "email": "user6@example.com",
                "invited_at": django.utils.timezone.now()
            }
        )

        obj = WaitlistEntry.objects.get(pk=response.data['id'])

        obj.invite()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        user = create_user(username="user6@example.com")

        user_response = self.client.post(
            reverse("log-in"),
            data={
                "username": "user6@example.com",
                "password": PASSWORD,
            },
        )

        # accept waitlist entry
        response = self.client.post(
            reverse("waitlist-accept", kwargs={'waitlist_entry_id': entry.id}),
            HTTP_AUTHORIZATION=f"Bearer {user_response.data['access']}"
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)