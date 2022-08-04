from rest_framework import permissions

from .utils import Role

class IsOrgAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `admin` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.org_relationships.get(org=obj).role.name == Role.ADMIN


class IsOrgMember(permissions.BasePermission):
    """
    Object-level permission to only allow members of an organization to read 
    the object.
    """

    def has_object_permission(self, request, view, obj):
        # Determine if user is admin of or in org being accessed
        return obj.pk in request.user.org_relationships.all().values_list('org__pk', flat=True)

class IsOrgMemberForInvitation(permissions.BasePermission):
    """
    Object-level permission to only allow members of an organization to read 
    the object.
    """

    def has_object_permission(self, request, view, obj):
        # Determine if user is admin of or in org being accessed
        return obj.org.pk in request.user.org_relationships.all().values_list('org__pk', flat=True)