import django

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

    admin = models.ForeignKey(
        "user.User", null=True, on_delete=models.CASCADE, related_name="admin"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("org-detail", kwargs={"org_id": self.pk})

    class Meta:
        ordering = ["created_at"]


class OrgRelationship(models.Model):
    REVOKED = "revoked"
    CUSTOMER = "customer"
    TEAM = "team"
    MANAGER = "manager"
    ADMIN = "admin"

    RELATIONSHIPS = (
        (REVOKED, "revoked"),
        (CUSTOMER, "Customer"),
        (TEAM, "Team"),
        (MANAGER, "Manager"),
        (ADMIN, "Admin"),
    )

    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name="relationships")
    related_user = models.ForeignKey("user.User", on_delete=models.CASCADE)

    relationship = models.CharField(
        max_length=256, choices=RELATIONSHIPS, default=CUSTOMER
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]


class OrgInvitation(models.Model):
    def save(self, *args, **kwargs):
        while not self.id or OrgInvitation.objects.filter(id=self.id).exists():
            self.id = id_generator()

        super(OrgInvitation, self).save(*args, **kwargs)

    id = models.CharField(primary_key=True, max_length=256, blank=True, unique=True)

    org = models.ForeignKey(
        "org.Org", null=True, on_delete=models.CASCADE, related_name="invitations"
    )

    invited_by = models.ForeignKey(
        "user.User", null=True, on_delete=models.CASCADE, related_name="invited_by"
    )
    invited_user = models.ForeignKey(
        "user.User", null=True, on_delete=models.CASCADE, related_name="invited_user"
    )

    expires_at = models.DateTimeField(null=True)
    accepted_at = models.DateTimeField(null=True)
    revoked_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("org-invitation-detail", kwargs={"org_invitation_id": self.pk})

    # Add the invited user to the org
    def accept(self, user):
        self.accepted_at = django.utils.timezone.now()
        self.invited_user = user

        # create the relationship
        org_relationship, created = OrgRelationship.objects.get_or_create(
            org=self.org, related_user=self.invited_user
        )

        # set the users role
        org_relationship.relationship = OrgRelationship.CUSTOMER
        org_relationship.save()

        # add the relationship to the user
        self.invited_user.org_relationships.add(org_relationship)
        self.save()

    # Revoke the invitation and kick a user out of the org
    def revoke(self):
        self.revoked_at = django.utils.timezone.now()
        self.save()

        if self.invited_user:
            # get the users relationship object
            org_relationship, created = OrgRelationship.objects.get_or_create(
                org=self.org, related_user=self.invited_user
            )

            # set the users role as revoked
            org_relationship.relationship = OrgRelationship.REVOKED
            org_relationship.save()

    class Meta:
        ordering = ["created_at"]
