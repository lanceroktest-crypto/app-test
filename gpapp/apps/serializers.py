from rest_framework import serializers
from .models import AppTestProfile, ScheduledTask, DeviceTestSession
from devices.serializers import AccountSerializer
from scripts.serializers import ScriptSerializer


class AppTestProfileSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    install_script_template_name = serializers.CharField(source='install_script_template.name', read_only=True)
    test_script_template_name = serializers.CharField(source='test_script_template.name', read_only=True)
    uninstall_script_template_name = serializers.CharField(source='uninstall_script_template.name', read_only=True)
    
    class Meta:
        model = AppTestProfile
        fields = '__all__'


class ScheduledTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledTask
        fields = '__all__'


class DeviceTestSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceTestSession
        fields = '__all__'