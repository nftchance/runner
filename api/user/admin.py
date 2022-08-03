from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import User

DefaultUserAdmin.fieldsets += (('Organization Management', {'fields': ('org_relationships', )}),)

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    pass