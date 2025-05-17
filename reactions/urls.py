from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ReactionViewSet, CommentViewSet

router = DefaultRouter()
router.register('reactions', ReactionViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]