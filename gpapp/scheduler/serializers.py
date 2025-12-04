from rest_framework import serializers
from .models import Schedule, DeviceSchedule
from apps.serializers import AppTestProfileSerializer
from devices.serializers import DeviceSerializer


class ScheduleSerializer(serializers.ModelSerializer):
    profile = AppTestProfileSerializer(read_only=True)
    
    class Meta:
        model = Schedule
        fields = '__all__'


class DeviceScheduleSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer(read_only=True)
    device = DeviceSerializer(read_only=True)
    
    class Meta:
        model = DeviceSchedule
        fields = '__all__'