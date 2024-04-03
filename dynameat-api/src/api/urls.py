from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SightingViewSet, UploadFileViewSet, AsteroidViewSet

router = DefaultRouter()
router.register(r'sightings', SightingViewSet, basename='sightings')
router.register(r'asteroids', AsteroidViewSet, basename='asteroids')
router.register(r'upload', UploadFileViewSet, basename='upload')

urlpatterns = [
    path('', include(router.urls)),
]
