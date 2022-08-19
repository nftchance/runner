from rest_framework import permissions


class CanManageOrg(permissions.BasePermission):
    """
    Make sure that only the select few permitted can manage the top-level of an org.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.user.has_perm("org.manage_org"):
            return True

        relationship_obj = request.user.org_relationships.filter(org=obj)
        if not relationship_obj.exists():
            return False
        return relationship_obj.first().has_perm("org.manage_org")


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
