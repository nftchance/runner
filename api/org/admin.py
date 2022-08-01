from django.contrib import admin

from .models import Org

@admin.register(Org)
class OrgAdmin(admin.ModelAdmin):
    fields = (
        "id",
        "name",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "name",
        "updated_at"
    )
    readonly_fields = ( 
        "id",
        "created_at",
        "updated_at"
    )