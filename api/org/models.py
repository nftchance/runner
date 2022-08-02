from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse 

from utils.uuid import id_generator

class Org(models.Model):
    def save(self, *args, **kwargs):
        while not self.id or Org.objects.filter(id=self.id).exists():
            self.id = id_generator()

        super(Org, self).save(*args, **kwargs)

    id = models.CharField(primary_key=True, max_length=256, blank=True, unique=True)

    name = models.CharField(max_length=256)

    admin = models.ForeignKey('user.User', null=True, on_delete=models.CASCADE, related_name="admin")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("org-detail", kwargs={"org_id": self.pk})
    
    class Meta:
        ordering = ["created_at"]
    
class OrgInvitation(models.Model):
    def save(self, *args, **kwargs):
        while not self.id or OrgInvitation.objects.filter(id=self.id).exists():
            self.id = id_generator()

        super(OrgInvitation, self).save(*args, **kwargs)

    id = models.CharField(primary_key=True, max_length=256, blank=True, unique=True)

    org = models.ForeignKey('org.Org', null=True, on_delete=models.CASCADE, related_name="invitations")

    invited_by = models.ForeignKey('user.User', null=True, on_delete=models.CASCADE, related_name="invited_by")
    invited_user = models.ForeignKey('user.User', null=True, on_delete=models.CASCADE, related_name="invited_user")

    expires_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('org-invitation-detail', kwargs={"org_invitation_id": self.pk})

    # Add the invited user to the org
    def accept(self, user):
        self.invited_user = user
        self.save()

        self.invited_user.orgs.add(self.org)
        self.invited_user.save()

    class Meta:
        ordering = ["created_at"]
