from django.test import TestCase

from org.models import Org

class OrgTest(TestCase):
    def test_org_create(self):
        org = Org.objects.create()
        self.assertNotEqual(org.id, None)