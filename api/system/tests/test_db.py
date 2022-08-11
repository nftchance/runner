from django.test import TestCase

from utils.tests.user import create_user

from org.permission_constants import org_permissions
from org.utils import load_permissions

from system.models import Broadcast

class BroadcastTestCase(TestCase):
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

