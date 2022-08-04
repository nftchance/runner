"""
Permissions managed:
- Manage Org
- Manage Org Roles
- Manage Org Invitations
"""

from org.utils import tiered_permissions

view_org = "view_org"

manage_roles = "manage_orgrole"
manage_org_invitations = "manage_orginvitation"
manage_org = "manage_org"

org_permissions = tiered_permissions(
    (
        [],
        [view_org],
        [],
        [manage_roles, manage_org_invitations],
        [manage_org],
    )
)
