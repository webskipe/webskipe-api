from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PageViewSet

router = DefaultRouter()
router.register('pages', PageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]