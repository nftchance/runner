import django

from django.contrib import auth
from django.contrib.auth.models import Permission
from django.db import models
from django.shortcuts import reverse
from django.utils.itercompat import is_iterable

from utils.uuid import OrgIDMixin

from . import backends
from .utils import Role


class Org(OrgIDMixin, models.Model):
    name = models.CharField(max_length=256)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("org-detail", kwargs={"org_id": self.pk})

    class Meta:
        ordering = ["created_at"]
        permissions = (
            ("manage_org", "Can manage organization"),
        )


class OrgRoleManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class OrgRole(models.Model):
    ROLES = (
        (Role.REVOKED, "Revoked"),
        (Role.CUSTOMER, "Customer"),
        (Role.TEAM, "Team"),
        (Role.MANAGER, "Manager"),
        (Role.ADMIN, "Admin"),
    )

    name = models.CharField(
        max_length=256, unique=True, choices=ROLES, default=Role.CUSTOMER
    )

    permissions = models.ManyToManyField(
        Permission,
        verbose_name="permissions",
        blank=True,
    )

    objects = OrgRoleManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

    class Meta:
        ordering = ["name"]


def _get_role():
    return OrgRole.objects.get_or_create(name="revoked")[0]


def _get_role_id():
    return _get_role().id


class OrgRelationship(models.Model):
    """
    Relationships define the level of access that a user has to an organization. These operate as the foundational level of permissioning. However, the relationships can be superceded by the permissions of the user.

    To accomplish this, a relationship stores the relationship status but additionally has dynamic permissions that are calculated based on the active modules within the organization.
    """

    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name="relationships")
    related_user = models.ForeignKey("user.User", on_delete=models.CASCADE)

    # immediately the role is set to revoked if not provided to prevent
    # the user from being able to access the organization if maliciously
    role = models.ForeignKey(
        OrgRole,
        on_delete=models.SET(_get_role),
        default=_get_role_id,
        related_name="relationship_set",
        related_query_name="relationship",
    )

    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        help_text="Permissions for the user of this relationship in this organization.",
        related_name="relationship_set",
        related_query_name="relationship",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("org-relationship-detail", kwargs={"org_id": self.org.pk, "org_relationship_id": self.pk})

    def get_user_permissions(self, obj=None):
        return backends.user_get_permissions(self, obj, "user")

    def get_role_permissions(self, obj=None):
        return backends.user_get_permissions(self, obj, "role")

    def get_all_permissions(self, obj=None):
        return backends.user_get_permissions(self, obj, "all")

    def has_perm(self, perm, obj=None):
        return backends.user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        if not is_iterable(perm_list) or isinstance(perm_list, str):
            raise ValueError("perm_list must be an iterable of permissions.")

        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        return backends.user_has_module_perms(self, app_label)

    def revoke(self):
        self.role = _get_role()
        self.permissions.clear()
        self.save()

    class Meta:
        ordering = ["created_at"]
        permissions = (
            ("manage_orgrelationship", "Can manage organization relationships of other users"),
        )

class OrgInvitation(OrgIDMixin, models.Model):
    org = models.ForeignKey(
        "org.Org", null=True, on_delete=models.CASCADE, related_name="invitations"
    )

    # if user is null, anyone will be able to join using the code
    invited_user = models.ForeignKey(
        "user.User", null=True, on_delete=models.CASCADE, related_name="invited_user"
    )
    role = models.CharField(
        max_length=256, choices=OrgRole.ROLES, default=Role.REVOKED
    )
    expires_at = models.DateTimeField(null=True)

    # automatically handled
    invited_by = models.ForeignKey(
        "user.User", null=True, on_delete=models.CASCADE, related_name="invited_by"
    )

    accepted_at = models.DateTimeField(null=True)
    revoked_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("org-invitation-detail", kwargs={"org_id": self.org.pk, "org_invitation_id": self.pk})

    # Add the invited user to the org
    def accept(self, user):
        self.accepted_at = django.utils.timezone.now()
        self.invited_user = user

        # create the relationship
        org_relationship = OrgRelationship.objects.get_or_create(
            org=self.org, related_user=self.invited_user
        )[0]

        # set the users role on the relationship object
        org_relationship_role = OrgRole.objects.get_or_create(name=self.role)[0]
        org_relationship.role = org_relationship_role
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
            org_relationship = OrgRelationship.objects.get_or_create(
                org=self.org, related_user=self.invited_user
            )[0]

            # set the users role as revoked
            org_relationship.role = OrgRole.objects.get_or_create(name="revoked")[0]
            org_relationship.save()

    class Meta:
        ordering = ["created_at"]
        permissions = (
            ("manage_orginvitation", "Can manage organization invitations"),
        )