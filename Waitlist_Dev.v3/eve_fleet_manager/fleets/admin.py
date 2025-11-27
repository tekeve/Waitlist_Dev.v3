from django.contrib import admin
from .models import Fleet, WaitlistEntry

@admin.register(Fleet)
class FleetAdmin(admin.ModelAdmin):
    list_display = ('name', 'fc', 'is_open', 'start_time')
    list_filter = ('is_open',)

@admin.register(WaitlistEntry)
class WaitlistEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'ship_name', 'role', 'is_accepted', 'fleet')
    list_filter = ('role', 'is_accepted', 'fleet')