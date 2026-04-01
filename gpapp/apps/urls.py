from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppTestProfileViewSet, ScheduledTaskViewSet, DeviceTestSessionViewSet

router = DefaultRouter()
router.register(r'apptestprofiles', AppTestProfileViewSet)
router.register(r'scheduledtasks', ScheduledTaskViewSet)
router.register(r'devicetestsessions', DeviceTestSessionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]