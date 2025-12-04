from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScriptViewSet

router = DefaultRouter()
router.register(r'scripts', ScriptViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]