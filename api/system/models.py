import django

from django.contrib.auth import get_user_model
from django.db import models

from utils.uuid import OrgIDMixin

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
    email = models.EmailField(max_length=100, unique=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    invited_at = models.DateTimeField(blank=True, null=True)
    invite_id = models.CharField(max_length=100, null=True, blank=True)

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
    
    def accept(self, user):
        if self.accepted_at:
            raise Exception("Already accepted")

        if user.email != self.email:
            raise Exception("Invite email does not match user email")

        self.user = user
        self.accepted_at = django.utils.timezone.now()
        self.save()

    class Meta:
        ordering = ['created_at']