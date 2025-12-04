from django.contrib import admin
from .models import AppTestProfile, ScheduledTask, DeviceTestSession
from devices.models import Account


@admin.register(AppTestProfile)
class AppTestProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'package_name', 'is_active', 'created_at']
    search_fields = ['name', 'package_name']
    list_filter = ['is_active', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    # Добавляем возможность выбора аккаунта
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "account":
            kwargs["queryset"] = Account.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ScheduledTask)
class ScheduledTaskAdmin(admin.ModelAdmin):
    list_display = ['profile', 'task_type', 'scheduled_time', 'executed', 'executed_at']
    search_fields = ['profile__name']
    list_filter = ['task_type', 'executed', 'scheduled_time']
    date_hierarchy = 'scheduled_time'


@admin.register(DeviceTestSession)
class DeviceTestSessionAdmin(admin.ModelAdmin):
    list_display = ['device', 'profile', 'start_date', 'end_date', 'current_task', 'status']
    search_fields = ['device__name', 'profile__name']
    list_filter = ['status', 'current_task', 'start_date']
    date_hierarchy = 'start_date'
