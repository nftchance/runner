from rest_framework import permissions

class IsOrgAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `admin` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.admin == request.user


class IsOrgMember(permissions.BasePermission):
    """
    Object-level permission to only allow members of an organization to read 
    the object.
    """

    def has_object_permission(self, request, view, obj):
        # Determine if user is admin of or in org being accessed
        return obj in request.user.orgs.all()