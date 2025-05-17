from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PageViewSet, page_reactions_summary

router = DefaultRouter()
router.register('pages', PageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('pages/<uuid:page_id>/reactions-summary/', page_reactions_summary, name='reactions-summary'),
]