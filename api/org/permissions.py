from rest_framework import permissions


class CanManageOrg(permissions.BasePermission):
    """
    Make sure that only the select few permitted can manage the top-level of an org.
    """

    def has_object_permission(self, request, view, obj):
        relationship_obj = request.user.org_relationships.filter(org=obj).first()
        if not relationship_obj:
            return False
        return relationship_obj.has_perm("org.manage_org")


class CanViewOrg(permissions.BasePermission):
    """
    Make sure that a user has the permission to view an organizations data.
    """

    def has_object_permission(self, request, view, obj):
        relationship_obj = request.user.org_relationships.filter(org=obj).first()
        if not relationship_obj:
            return False
        return relationship_obj.has_perm("org.view_org")

class CanManageOrgRelationship(permissions.BasePermission):
    """
    Make sure that the requesting user has the ability to control the relationship permissions and roles within an org.
    """

    def has_permission(self, request, view):
        relationship_obj = request.user.org_relationships.filter(
            org=request.resolver_match.kwargs.get("org_id")
        ).first()
        if not relationship_obj:
            return False

        return relationship_obj.has_perm("org.manage_orgrelationship")

    # def has_object_permission(self, request, view, obj):
    #     # TODO: This is an incorrect implementation of checking the permissions since this is checking the permission of the active relationship rather than the relationship that is being used to retrieve this dataset from the datbase.
    #     relationship_obj = request.user.org_relationships.filter(org=obj.org).first()
    #     if not relationship_obj:
    #         return False
    #     return relationship_obj.has_perm("org.manage_org_relationship")

class CanManageOrgInvitiation(permissions.BasePermission):
    """
    Make sure that the requesting user has the ability to control invitations for an org.
    """

    def has_permission(self, request, view):
        relationship_obj = request.user.org_relationships.filter(
            org=request.resolver_match.kwargs.get("org_id")
        ).first()
        if not relationship_obj:
            return False

        return relationship_obj.has_perm("org.manage_orginvitation")