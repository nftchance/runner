from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from org.models import Org

from utils.tests.user import PASSWORD, create_user

from org.models import Org

class HttpTest(APITestCase):
    def setUp(self):
        user = create_user()
        response = self.client.post(reverse('log_in'), data={
            'username': user.username,
            'password': PASSWORD,
        })
        self.access = response.data['access']

    def test_user_can_list_orgs(self):
        orgs = [
            Org.objects.create(name="Simpler Times"),
            Org.objects.create(name="Simplest Times")
        ]
        response = self.client.get(reverse('org_list'),
            HTTP_AUTHORIZATION=f'Bearer {self.access}'
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        exp_org_ids = [str(org.id) for org in orgs]
        act_org_ids = [org.get('id') for org in response.data]
        self.assertCountEqual(exp_org_ids, act_org_ids)

    def test_user_can_retrieve_org_by_id(self):
        org = Org.objects.create(name="Simpler Times")
        response = self.client.get(org.get_absolute_url(),
            HTTP_AUTHORIZATION=f'Bearer {self.access}'
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(str(org.id), response.data.get('id'))