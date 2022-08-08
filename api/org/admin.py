from django.contrib import admin

from .models import Org, OrgInvitation, OrgRelationship, OrgRole


@admin.register(Org)
class OrgAdmin(admin.ModelAdmin):
    fields = (
        "id",
        "name",
        "created_at",
        "updated_at",
    )
    list_display = ("id", "name", "updated_at")
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(OrgInvitation)
class OrgInvitationAdmin(admin.ModelAdmin):
    fields = (
        "id",
        "org",
        "invited_user",
        "role",
        "expires_at",
        "invited_by",
        "accepted_at",
        "revoked_at",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "org",
        "role",
        "expires_at",
        "invited_by",
        "invited_user",
        "accepted_at",
        "revoked_at",
        "updated_at",
    )
    readonly_fields = (
        "id",
        "invited_by",
        "created_at",
        "updated_at",
        "accepted_at",
        "revoked_at",
    )


@admin.register(OrgRelationship)
class OrgRelationshipAdmin(admin.ModelAdmin):
    fields = (
        "id",
        "org",
        "related_user",
        "role",
        "permissions",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "org",
        "related_user",
        "role",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(OrgRole)
class OrgRoleAdmin(admin.ModelAdmin):
    fields = (
        "id",
        "name",
        "permissions",
    )
    list_display = (
        "id",
        "name",
    )
    readonly_fields = ("id",)
