from django.contrib import admin
from .models import Schedule, DeviceSchedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['profile', 'start_date', 'end_date', 'is_active', 'created_at']
    search_fields = ['profile__name']
    list_filter = ['is_active', 'start_date', 'end_date']
    date_hierarchy = 'created_at'


@admin.register(DeviceSchedule)
class DeviceScheduleAdmin(admin.ModelAdmin):
    list_display = ['schedule', 'device', 'assigned_at']
    search_fields = ['schedule__profile__name', 'device__name']
    list_filter = ['assigned_at']
    date_hierarchy = 'assigned_at'
