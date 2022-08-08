from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from utils.tests.user import PASSWORD, create_user

from job.models import Job

class HttpTest(APITestCase):
    def setUp(self):
        user = create_user()
        response = self.client.post(reverse('log-in'), data={
            'username': user.username,
            'password': PASSWORD,
        })
        self.access = response.data['access']

    def test_user_can_list_jobs(self):
        jobs = [
            Job.objects.create(),
            Job.objects.create()
        ]
        response = self.client.get(reverse('job_list'),
            HTTP_AUTHORIZATION=f'Bearer {self.access}'
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        exp_job_ids = [str(job.id) for job in jobs]
        act_job_ids = [job.get('id') for job in response.data]
        self.assertCountEqual(exp_job_ids, act_job_ids)

    def test_user_can_retrieve_job_by_id(self):
        job = Job.objects.create()
        response = self.client.get(job.get_absolute_url(),
            HTTP_AUTHORIZATION=f'Bearer {self.access}'
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(str(job.id), response.data.get('id'))