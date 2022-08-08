from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import Permission

from .models import User

DefaultUserAdmin.fieldsets += (
    ("Organization Management", {"fields": ("org_relationships",)}),
)


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    pass


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass
