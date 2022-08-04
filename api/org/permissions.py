from rest_framework import permissions

from .models import OrgInvitation

class CanManageOrg(permissions.BasePermission):
    """
    Make sure that only the select few permitted can manage the top-level of an org.
    """

    def has_object_permission(self, request, view, obj):
        relationship_obj = request.user.org_relationships.filter(org=obj).first()
        if not relationship_obj:
            return False
        return relationship_obj.has_perm('org.manage_org')


class CanViewOrg(permissions.BasePermission):
    """
    Make sure that a user has the permission to view an organizations data.
    """

    def has_object_permission(self, request, view, obj):
        relationship_obj = request.user.org_relationships.filter(org=obj).first()
        if not relationship_obj:
            return False
        return relationship_obj.has_perm('org.view_org')

class CanManageOrgInvitiation(permissions.BasePermission):
    """
    Make sure that the requesting user has the ability to control invitations for an org.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, OrgInvitation):
            relationship_obj = request.user.org_relationships.filter(org=obj.org).first()
        else: 
            relationship_obj = request.user.org_relationships.filter(org=obj).first()
        
        if not relationship_obj:
            return False
        return relationship_obj.has_perm('org.manage_orginvitation')