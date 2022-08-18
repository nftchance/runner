from rest_framework import permissions


class CanManageUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authentiated:
            return False

        if request.user.has_permission('user.manage_user'):
            return True

        return request.user == obj
