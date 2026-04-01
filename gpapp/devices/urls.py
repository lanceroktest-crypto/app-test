from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet, AccountViewSet, DeviceAccountViewSet

router = DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'device-accounts', DeviceAccountViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]