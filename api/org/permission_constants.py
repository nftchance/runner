"""
Permissions managed:
- Manage Org
- Manage Org Roles
- Manage Org Invitations
"""

class Role:
    REVOKED = "revoked"
    CUSTOMER = "customer"
    TEAM = "team"
    MANAGER = "manager"
    ADMIN = "admin"

manage_roles = "manage_orgrole"
manage_org_invitations = "manage_orginvitation"
manage_org = "manage_org"

# Building the role permissions.
revoked_role_permissions = []
customer_role_permissions = []
team_role_permissions = []
manager_role_permissions = [manage_roles, manage_org_invitations]
admin_role_permissions = manager_role_permissions + [manage_org]

# Final output of this apps permission structure.
org_permissions = {
    'revoked': revoked_role_permissions,
    'customer': customer_role_permissions,
    'team': team_role_permissions,
    'manager': manager_role_permissions,
    'admin': admin_role_permissions,
}