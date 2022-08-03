"""
Permissions managed:
- Manage Org
- Manage Org Roles
- Manage Org Invitations
"""

from org.utils import tiered_permissions


manage_roles = "manage_orgrole"
manage_org_invitations = "manage_orginvitation"
manage_org = "manage_org"


# Building the role permissions.
permissions = tiered_permissions(
    (
        [],
        [],
        [],
        [manage_roles, manage_org_invitations],
        [manage_org],
    )
)

# Final output of this apps permission structure.
org_permissions = {
    "revoked": permissions[0],
    "customer": permissions[1],
    "team": permissions[2],
    "manager": permissions[3],
    "admin": permissions[4],
}
