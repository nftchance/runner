from django.db import models

from org.models import Org

class ScheduleQuerySet(models.QuerySet):
    def schedules_for_org(self, org):
        return self.filter(org=org)

class ScheduleManager(models.Manager):
    def get_queryset(self):
        return ScheduleQuerySet(self.model, using=self._db)

    def schedules_for_org(self, org):
        return self.get_queryset().schedules_for_org(org)

class Schedule(models.Model):
    archived = models.BooleanField(default=False)
    
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    priority = models.PositiveIntegerField(default=0)

    seconds_after = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ScheduleManager()

    class Meta:
        ordering = ['priority']