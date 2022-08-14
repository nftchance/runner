from rest_framework import permissions

class CanManageBroadcast(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("system.manage_broadcast")

class CanManageWaitlistEntry(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("system.manage_waitlistentry")
