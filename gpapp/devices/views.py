from django.shortcuts import render
from rest_framework import viewsets
from .models import Device, Account, DeviceAccount
from .serializers import DeviceSerializer, AccountSerializer, DeviceAccountSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class DeviceAccountViewSet(viewsets.ModelViewSet):
    queryset = DeviceAccount.objects.all()
    serializer_class = DeviceAccountSerializer
