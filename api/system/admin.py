from django.contrib import admin

from .models import Broadcast

@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_text', 'link_url', 'external', 'expired_at', 'created_at', 'updated_at')
    list_filter = ('expired_at', 'created_at', 'updated_at')
    search_fields = ('title', 'link_text', 'link_url')
    read_only_fields = ('created_at', 'updated_at')