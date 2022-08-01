from django.contrib import admin

from .models import Schedule

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    fields = (
        "archived",
        "id",
        "org",
        "priority",
        "seconds_after",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "priority",
        "seconds_after",
        "updated_at"
    )
    readonly_fields = ( 
        "id",
        "created_at",
        "updated_at"
    )