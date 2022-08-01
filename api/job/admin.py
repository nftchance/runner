from django.contrib import admin

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    fields = (
        "archived",
        "draft",
        "id",
        "org",
        "time",
        "schedule",
        "status",
        "created_at",
        "updated_at",
    )
    list_display = (
        "archived",
        "draft",
        "id",
        "status",
        "updated_at",
    )
    list_filter = ("status",)
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
