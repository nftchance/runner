import os

from django.apps import AppConfig

from org.permission_constants import org_permissions


class OrgConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "org"

    def load_permissions(self, roles_permissions):
        """
        Loads the custom permissions defined in the org app onto the organization roles.
        """

        from django.contrib.auth.models import Permission

        from org.models import OrgRole

        # load the constant-provided permissions for each role into the database
        for role_name, permissions in roles_permissions.items():
            role = OrgRole.objects.get_or_create(name=role_name)[0]
            for permission_name in permissions:
                permission = Permission.objects.get(codename=permission_name)
                role.permissions.add(permission)
            role.save()

    def ready(self):
        # load the custom permission framework
        if os.environ.get("RUN_MAIN"):
            self.load_permissions(org_permissions)