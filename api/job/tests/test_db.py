# import datetime
# import django

# from django.test import TestCase

# from job.models import Job
# from org.models import Org
# from schedule.models import Schedule

# class JobTestCase(TestCase):
#     def setUp(self):
#         self.org = Org.objects.create(
#             name="RUNNER MOCK"
#         )
#         self.job = Job.objects.create(org=self.org)

#     def test_job_create(self):
#         job = Job.objects.create(org=self.org)
#         self.assertNotEqual(job.id, None)

#     def test_job_id_overlap_prevention(self):
#         job = Job.objects.create(org=self.org)
#         job_overlap = Job.objects.create(org=self.org, id=job.id)
#         self.assertNotEqual(job.id, job_overlap.id)

#     def test_schedule_next_time(self):
#         self.job.schedule = Schedule.objects.create(seconds_after=120, org=self.org)
#         self.assertEqual(self.job.next_time, None)

#         self.job.time = django.utils.timezone.now() + datetime.timedelta(hours=6)
#         self.job.save()
#         next_time = self.job.time + datetime.timedelta(seconds=120)

#         self.assertEqual(
#             (self.job.next_time.hour, self.job.next_time.minute), 
#             (next_time.hour, next_time.minute) 
#         )

#     def test_job_seconds_until_time(self):
#         self.assertEqual(self.job.seconds_until_time, None)

#         self.job.time = django.utils.timezone.now() + datetime.timedelta(hours=6)
#         self.job.save()

#         self.assertEqual(21599,  self.job.seconds_until_time)