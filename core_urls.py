from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LatticeDesignViewSet

router = DefaultRouter()
router.register(r'lattices', LatticeDesignViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
