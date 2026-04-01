from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduleViewSet, DeviceScheduleViewSet

router = DefaultRouter()
router.register(r'schedules', ScheduleViewSet)
router.register(r'deviceschedules', DeviceScheduleViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]