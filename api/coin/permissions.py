from rest_framework import permissions


class CanManageTransfer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("coin.manage_transfer")
