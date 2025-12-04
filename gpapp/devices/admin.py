from django.contrib import admin
from .models import Device, Account, DeviceAccount


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'udid', 'status', 'is_active', 'created_at']
    search_fields = ['name', 'udid']
    list_filter = ['status', 'is_active', 'created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'created_at']
    search_fields = ['email']
    list_filter = ['is_active', 'created_at']
    readonly_fields = ['created_at', 'updated_at']


class DeviceAccountInline(admin.TabularInline):
    model = DeviceAccount
    extra = 1


@admin.register(DeviceAccount)
class DeviceAccountAdmin(admin.ModelAdmin):
    list_display = ['device', 'account']
    list_filter = ['device', 'account']
