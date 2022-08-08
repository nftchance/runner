class Role:
    REVOKED = "revoked"
    CUSTOMER = "customer"
    TEAM = "team"
    MANAGER = "manager"
    ADMIN = "admin"

def tiered_permissions(permissions):
    return {
        "revoked": permissions[0],
        "customer": permissions[1],
        "team": permissions[1] + permissions[2],
        "manager": permissions[1] + permissions[2] + permissions[3],
        "admin": permissions[1] + permissions[2] + permissions[3] + permissions[4],
    }

def load_permissions(app_label, roles_permissions):
    """
    Loads the custom permissions defined in the org app onto the organization roles.
    """

    from django.contrib.auth.models import Permission

    from org.models import OrgRole

    for role_name, permissions in roles_permissions.items():
        role = OrgRole.objects.get_or_create(name=role_name)[0]
        role_permissions = role.permissions.filter(content_type__app_label=app_label)
        role.permissions.remove(*role_permissions)

        for permission_name in permissions:
            permission = Permission.objects.get(codename=permission_name)
            role.permissions.add(permission)
        role.save()