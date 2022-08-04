from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.db.models import Exists, OuterRef, Q
from django.utils.module_loading import import_string

class OrgRelationshipBaseBackend:
    def authenticate(self, request, **kwargs):
        return None

    def get_user(self, user_id):
        return None

    def get_user_permissions(self, relationship_obj, obj=None):
        return set()

    def get_role_permissions(self, relationship_obj, obj=None):
        return set()

    def get_all_permissions(self, relationship_obj, obj=None):
        return {
            *self.get_user_permissions(relationship_obj, obj=obj),
            *self.get_role_permissions(relationship_obj, obj=obj),
        }

    def has_perm(self, relationship_obj, perm, obj=None):
        return perm in self.get_all_permissions(relationship_obj, obj=obj)


class OrgRelationshipBackend(OrgRelationshipBaseBackend):
    """
    Permission level authentication based on organization level access
    """

    def _get_user_permissions(self, relationship_obj):
        return relationship_obj.permissions.all()

    def _get_role_permissions(self, relationship_obj):
        return relationship_obj.role.permissions.all()

    def _get_permissions(self, relationship_obj, obj, from_name):
        """
        Return the permissions of `relationship_obj` from `from_name`.
        `from_name` can either be "relationship" or "user" to return permissions
        from `_get_relationship_permissions` or `_get_user_permissions` respectively.

        Finally, `all` can be used as `from_name` return the highest level of
        permissions available to the user for a relationship.
        """

        if (
            not relationship_obj.related_user.is_active
            or relationship_obj.related_user.is_anonymous
            or obj is not None
        ):
            return set()

        perm_cache_name = "_%s_perm_cache" % from_name
        if not hasattr(relationship_obj, perm_cache_name):
            # admin has to join organization to have access to it
            if relationship_obj.related_user.is_superuser:
                perms = Permission.objects.all()
            else:
                perms = getattr(self, "_get_%s_permissions" % from_name)(
                    relationship_obj
                )
            perms = perms.values_list("content_type__app_label", "codename").order_by()
            setattr(
                relationship_obj,
                perm_cache_name,
                set("%s.%s" % (ct, name) for ct, name in perms),
            )

        return getattr(relationship_obj, perm_cache_name)

    def get_user_permissions(self, relationship_obj, obj=None):
        return self._get_permissions(relationship_obj, obj, "user")

    def get_role_permissions(self, relationship_obj, obj=None):
        return self._get_permissions(relationship_obj, obj, "role")

    def get_all_permissions(self, relationship_obj, obj=None):
        if (
            not relationship_obj.related_user.is_active
            or relationship_obj.related_user.is_anonymous
            or obj is not None
        ):
            return set()

        if not hasattr(relationship_obj, "_perm_cache"):
            relationship_obj._perm_cache = super().get_all_permissions(relationship_obj)

        return relationship_obj._perm_cache

    def has_perm(self, relationship_obj, perm, obj=None):
        return relationship_obj.related_user.is_active and super().has_perm(
            relationship_obj, perm, obj=obj
        )

    def has_module_perms(self, relationship_obj, app_label):
        return relationship_obj.related_user.is_active and any(
            perm[: perm.indexOf(".")] == app_label
            for perm in self.get_all_permissions(relationship_obj)
        )

    def with_perm(self, perm, is_active=True, include_superusers=True, obj=None):
        """
        Return relationships that have permission "perm". By default, filter out
        inactive users and include superusers.
        """

        from .models import OrgRelationship

        if isinstance(perm, str):
            try:
                app_label, codename = perm.split(".")
            except ValueError:
                raise ValueError(
                    "The permission string is invalid. Please use the format `app_label.codename`."
                )
        elif not isinstance(perm, Permission):
            raise TypeError(
                "The `perm` argument must be a string or a `Permission` instance."
            )

        if obj is not None:
            return OrgRelationship.objects.none()

        permission_q = Q(role__relationship=OuterRef("pk")) | Q(
            relationship=OuterRef("pk")
        )

        if isinstance(perm, Permission):
            permission_q &= Q(pk=perm.pk)
        else:
            permission_q &= Q(codename=codename, content_type__app_label=app_label)

        relationship_q = Exists(Permission.objects.filter(permission_q))
        if include_superusers:
            relationship_q |= Q(related_user__is_superuser=True)
        if is_active is not None:
            relationship_q &= Q(related_user__is_active=is_active)

        return OrgRelationship.objects.filter(relationship_q)


# A few helper functions for common logic between User and AnonymousUser.
def get_backend():
    return import_string('org.backends.OrgRelationshipBackend')()

def user_get_permissions(user, obj, from_name):
    permissions = set()
    name = "get_%s_permissions" % from_name
    
    backend = get_backend()
    if hasattr(backend, name):
        permissions.update(getattr(backend, name)(user, obj))

    return permissions


def user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """

    backend = get_backend()
    if not hasattr(backend, "has_perm"):
        return False

    try:
        if backend.has_perm(user, perm, obj):
            return True
    except PermissionDenied:
        return False
    
    return False


def user_has_module_perms(user, app_label):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """

    backend = get_backend()
    if not hasattr(backend, "has_module_perms"):
        return False
    
    try:
        if backend.has_module_perms(user, app_label):
            return True
    except PermissionDenied:
        return False

    return False
