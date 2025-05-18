from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from django.db.models import Count

from reactions.models import Reaction
from .models import Page, PageMedia
from .serializers import (
    PageSerializer,
    PageCreateSerializer,
    PageListSerializer,
    PageMediaSerializer,
)
from .permissions import IsOwnerOrReadOnly

class PageViewSet(viewsets.ModelViewSet):
    """View for managing page APIs"""
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tone', 'template', 'status', 'privacy']
    search_fields = ['title', 'context', 'message']
    ordering_fields = ['created_at', 'views', 'title']
    
    def get_queryset(self):
        """Return objects for the current authenticated user or public pages"""
        if self.action == 'list':
            if self.request.query_params.get('me') == 'true':
                # Only show the current user's pages if requested
                return self.queryset.filter(user=self.request.user)
            # For public list, only show published, public pages
            return self.queryset.filter(status='published', privacy='public')
        return self.queryset
    
    def retrieve(self, request, slug=None):
        page = Page.objects.get(slug=slug)
        serializer = self.get_serializer(page)
        return Response(serializer.data)
    
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list':
            return PageListSerializer
        if self.action == 'create':
            return PageCreateSerializer
        return self.serializer_class
    
    @action(detail=True, methods=['post'])
    def increment_view(self, request, slug=None):
        """Increment the view counter for a page"""
        page = self.get_object()
        page.views += 1
        page.save()
        return Response({'status': 'views incremented'})
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def upload_media(self, request, slug=None):
        """Upload media to a page"""
        page = self.get_object()
        
        # Check if the user is the owner of the page
        if request.user != page.user:
            return Response(
                {'error': 'You cannot upload media to this page'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response(
                {'error': 'No file found in request'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file_type = request.data.get('file_type', 'image')
        
        media = PageMedia.objects.create(
            page=page,
            file=file_obj,
            file_type=file_type
        )
        
        serializer = PageMediaSerializer(media)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


@api_view(['GET'])
def page_reactions_summary(request, page_id):
    reactions = Reaction.objects.filter(page_id=page_id) \
        .values('reaction_type') \
        .annotate(count=Count('id')) \
        .order_by('-count')
    return Response(reactions)