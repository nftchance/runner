import datetime

from django.db import models

from utils.time import seconds_until
from utils.uuid import id_generator

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


class Job(models.Model):
    def save(self, *args, **kwargs):
        while not self.id or Job.objects.filter(id=self.id).exists():
            self.id = id_generator()

        super(Job, self).save(*args, **kwargs)

    archived = models.BooleanField(default=False)

    id = models.CharField(primary_key=True, max_length=256, blank=True, unique=True)
    org = models.ForeignKey(Org, null=False, on_delete=models.CASCADE)

    draft = models.BooleanField(default=True)
    time = models.DateTimeField(blank=True, null=True)

    schedule = models.ForeignKey(Schedule, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = JobsManager()

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
