from django.shortcuts import render
from rest_framework import viewsets
from .models import AppTestProfile, ScheduledTask, DeviceTestSession
from .serializers import AppTestProfileSerializer, ScheduledTaskSerializer, DeviceTestSessionSerializer


class AppTestProfileViewSet(viewsets.ModelViewSet):
    queryset = AppTestProfile.objects.all()
    serializer_class = AppTestProfileSerializer


class ScheduledTaskViewSet(viewsets.ModelViewSet):
    queryset = ScheduledTask.objects.all()
    serializer_class = ScheduledTaskSerializer


class DeviceTestSessionViewSet(viewsets.ModelViewSet):
    queryset = DeviceTestSession.objects.all()
    serializer_class = DeviceTestSessionSerializer
