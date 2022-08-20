import django

from rest_framework import permissions

class CanManageProposal(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated: return False

        if request.user.is_authenticated and request.user.has_perm('governance.manage_proposal'):
            return True
        
        return obj.proposed_by == request.user and obj.approved_at >= django.utils.timezone.now()

class CanProgressProposal(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated: return False

        if request.user.is_authenticated and request.user.has_perm('governance.manage_proposal'):
            return True
        
        return False