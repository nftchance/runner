import django
import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from utils.uuid import OrgIDMixin

from .utils import WAITLIST_PERIOD_DURATION_HOURS, WAITLIST_PERIOD_ENTRIES

User = get_user_model()

class Broadcast(models.Model):
    title = models.CharField(max_length=100)
    link_text = models.CharField(max_length=100)
    link_url = models.CharField(max_length=100)
    external = models.BooleanField(default=False)

    expired_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class WaitlistEntry(OrgIDMixin, models.Model):
    def save(self, *args, **kwargs):
        # filter out the +tags of an email
        if self.email and "+" in self.email:
            self.email = re.sub(r"([+])\w+", "", self.email)

        super(WaitlistEntry, self).save(*args, **kwargs)

    email = models.EmailField(max_length=100, unique=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    invited_at = models.DateTimeField(blank=True, null=True)

    accepted_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
    
    def invite(self):
        # send notifications to the invited email
        if self.invited_at != None:
            raise Exception("Already invited")

        self.invited_at = django.utils.timezone.now()
        self.save()
    
    def can_accept(self):
        return not WaitlistEntry.objects.filter(accepted_at__gte=django.utils.timezone.now() - django.utils.timezone.timedelta(hours=WAITLIST_PERIOD_DURATION_HOURS)).count() >= WAITLIST_PERIOD_ENTRIES

    def accept(self, user):
        if not self.can_accept():
            raise Exception("Waitlist redemption limit reached")

        if self.accepted_at:
            raise Exception("Already accepted")

        if user.email != self.email:
            raise Exception("Invite email does not match user email")

        self.user = user
        self.accepted_at = django.utils.timezone.now()
        self.save()

    def time_until_can_accept(self):
        if self.accepted_at:
            return None

        if self.invited_at == None:
            return None

        if self.can_accept():
            return 0

        # get the 5 most recent waitlist entries that have been accepted
        accepted_entries = WaitlistEntry.objects.filter(accepted_at__gte=django.utils.timezone.now() - django.utils.timezone.timedelta(hours=WAITLIST_PERIOD_DURATION_HOURS)).order_by("accepted_at")[:WAITLIST_PERIOD_ENTRIES]

        if accepted_entries.exists():
            # get difference between now and accepted_at + 24 hours of the first object in the queryset
            return (django.utils.timezone.now() - accepted_entries.first().accepted_at) + django.utils.timezone.timedelta(hours=WAITLIST_PERIOD_DURATION_HOURS)

        return 0

    class Meta:
        ordering = ['created_at']