import os

from django.apps import AppConfig

from org.permission_constants import org_permissions


class OrgConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "org"

    def load_permissions(self, app_label, roles_permissions):
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

    def ready(self):
        # load the custom permission framework
        if os.environ.get("RUN_MAIN"):
            self.load_permissions("org", org_permissions)