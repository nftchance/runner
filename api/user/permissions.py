from rest_framework import permissions


class CanManageUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.user.has_perm('user.manage_user'):
            return True

        return request.user == obj
