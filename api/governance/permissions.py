from rest_framework import permissions

class CanManageProposal(permissions.BasePermission):
    def has_obj_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.has_perm('proposal.manage_proposal'):
            return True
        
        return obj.proposed_by == request.user or obj.approved