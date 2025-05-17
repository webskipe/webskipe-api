from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .models import Reaction, Comment
from .serializers import ReactionSerializer, CommentSerializer
from pages.permissions import IsOwnerOrReadOnly

class ReactionViewSet(viewsets.ModelViewSet):
    """View for managing reaction APIs"""
    serializer_class = ReactionSerializer
    queryset = Reaction.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['page', 'reaction_type']
    
    def perform_create(self, serializer):
        """Create a new reaction"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def toggle(self, request):
        """Toggle a reaction (add/remove)"""
        page_id = request.data.get('page')
        reaction_type = request.data.get('reaction_type')
        
        if not page_id or not reaction_type:
            return Response(
                {'error': 'page and reaction_type are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if the reaction already exists
        reaction = Reaction.objects.filter(
            user=request.user,
            page_id=page_id,
            reaction_type=reaction_type
        ).first()
        
        if reaction:
            # Remove the existing reaction
            reaction.delete()
            return Response({'status': 'reaction removed'})
        else:
            # Create a new reaction
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentViewSet(viewsets.ModelViewSet):
    """View for managing comment APIs"""
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['page']
    
    def perform_create(self, serializer):
        """Create a new comment"""
        serializer.save(user=self.request.user)