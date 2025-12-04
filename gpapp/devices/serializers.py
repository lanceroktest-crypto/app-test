from rest_framework import serializers
from .models import Device, Account, DeviceAccount


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class DeviceAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceAccount
        fields = '__all__'