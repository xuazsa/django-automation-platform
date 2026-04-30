from django.contrib import admin
from .models import Switch

@admin.register(Switch)
class SwitchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ip_address', 'vendor', 'status', 'last_seen')
    list_filter = ('vendor', 'status')
    search_fields = ('name', 'ip_address')
