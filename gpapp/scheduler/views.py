from django.shortcuts import render
from rest_framework import viewsets
from .models import Schedule, DeviceSchedule
from .serializers import ScheduleSerializer, DeviceScheduleSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class DeviceScheduleViewSet(viewsets.ModelViewSet):
    queryset = DeviceSchedule.objects.all()
    serializer_class = DeviceScheduleSerializer
