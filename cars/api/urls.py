from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import AutoViewsSet, OwnerViewSet


router = DefaultRouter()
router.register('autos', AutoViewsSet)
router.register('owners', OwnerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
