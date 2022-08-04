import os

from django.apps import AppConfig

from org.permission_constants import org_permissions
from org.utils import load_permissions

class OrgConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "org"

    def ready(self):
        # load the custom permission framework
        load_permissions("org", org_permissions)