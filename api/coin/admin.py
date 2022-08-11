from django.contrib import admin

from .models import Coin

@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin): 
    list_display = ('name', 'symbol', 'created_at', 'updated_at')
    search_fields = ('name', 'symbol')