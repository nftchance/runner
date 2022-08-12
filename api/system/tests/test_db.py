import django

from django.db.utils import IntegrityError
from django.test import TestCase

from utils.tests.user import create_user

from org.permission_constants import org_permissions
from org.utils import load_permissions

from system.models import Broadcast, WaitlistEntry

class SystemTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.secondary_user = create_user(username="secondaryuser@example.com")        
        
        load_permissions("org", org_permissions)

    def test_create_broadcast(self):
        Broadcast.objects.create(
            title="Test Broadcast",
            link_text="Test Link Text",
            link_url="http://example.com",
            expired_at=None,
            external=True
        )

        self.assertEqual(Broadcast.objects.count(), 1)

    def test_create_waitlist_entry(self):
        WaitlistEntry.objects.create(
            email="user@example.com"
        )

        self.assertEqual(WaitlistEntry.objects.count(), 1)

    def test_cannot_create_waitlist_entry_for_same_email_address_twice(self):
        WaitlistEntry.objects.create(
            email="user@example.com"
        )

        # make sure create errors out due to email not being unique
        with self.assertRaises(IntegrityError):
            WaitlistEntry.objects.create(
                email="user@example.com"
            )

    # def test_cannot_create_waitlist_entry_twice_with_salted_email(self):
    #     WaitlistEntry.objects.create(
    #         email="user@example.com"
    #     )

    #     with self.assertRaises(Exception):
    #         WaitlistEntry.objects.create(
    #             email="user+test@example.com"
    #         )

    def test_can_invite_waitlist_entry(self):
        entry = WaitlistEntry.objects.create(
            email="inviteuser@example.com"
        )

        entry.invite()

        self.assertEqual(WaitlistEntry.objects.count(), 1)
        self.assertIsNotNone(entry.invited_at)

    def test_user_can_accept_invitation(self):
        entry = WaitlistEntry.objects.create(
            email="user@example.com")

        entry.invite()
        entry.accept(self.user)

        self.assertIsNotNone(entry.user)
        self.assertIsNotNone(entry.accepted_at)

    def test_user_cannot_accept_invitation_twice(self):
        entry = WaitlistEntry.objects.create(
            email="user@example.com")

        entry.invite()

        entry.accept(self.user)

        self.assertIsNotNone(entry.user)
        self.assertIsNotNone(entry.accepted_at) 
        
        with self.assertRaises(Exception):
            entry.accept(self.user)

    def test_user_cannot_accept_invitation_for_different_email(self):
        entry = WaitlistEntry.objects.create(
            email="userbigdog@example.com")

        entry.invite()

        with self.assertRaises(Exception):
            entry.accept(self.user)