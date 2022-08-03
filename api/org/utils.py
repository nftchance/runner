class Role:
    REVOKED = "revoked"
    CUSTOMER = "customer"
    TEAM = "team"
    MANAGER = "manager"
    ADMIN = "admin"

def tiered_permissions(permissions):
    return (
        permissions[0],
        permissions[1],
        permissions[1] + permissions[2],
        permissions[1] + permissions[2] + permissions[3],
        permissions[1] + permissions[2] + permissions[3] + permissions[4],
    )
