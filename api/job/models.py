import datetime

from django.db import models
from django.shortcuts import reverse

from utils.time import seconds_until
from utils.uuid import OrgIDMixin

from org.models import Org
from schedule.models import Schedule


class JobsQuerySet(models.QuerySet):
    def jobs_for_org(self, org):
        return self.filter(org=org)


class JobsManager(models.Manager):
    def get_queryset(self):
        return JobsQuerySet(self.model, using=self._db)

    def jobs_for_org(self, org):
        return self.get_queryset().jobs_for_org(org)


class Job(OrgIDMixin, models.Model):
    REQUESTED = "REQUESTED"
    UPCOMING = "UPCOMING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    STATUSES = (
        (REQUESTED, REQUESTED),
        (UPCOMING, UPCOMING),
        (IN_PROGRESS, IN_PROGRESS),
        (COMPLETED, COMPLETED),
    )

    archived = models.BooleanField(default=False)

    org = models.ForeignKey(Org, blank=False, null=True, on_delete=models.CASCADE)

    draft = models.BooleanField(default=True)
    time = models.DateTimeField(blank=True, null=True)

    schedule = models.ForeignKey(Schedule, null=True, on_delete=models.SET_NULL)

    status = models.CharField(max_length=20, choices=STATUSES, default=REQUESTED)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = JobsManager()

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse("job_detail", kwargs={"job_id": self.pk})
    
    @property
    def next_time(self):
        if not self.time or not self.schedule.seconds_after:
            return None
        return self.time + datetime.timedelta(seconds=self.schedule.seconds_after)

    @property
    def seconds_until_time(self):
        return seconds_until(self.time)

    @property
    def seconds_until_next_time(self):
        return seconds_until(self.next_time)

    class Meta:
        ordering = ["created_at"]
