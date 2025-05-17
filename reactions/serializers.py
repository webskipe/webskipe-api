from rest_framework import serializers
from .models import Reaction, Comment
from users.serializers import UserSerializer

class ReactionSerializer(serializers.ModelSerializer):
    """Serializer for the reaction object"""
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Reaction
        fields = ('id', 'user', 'page', 'reaction_type', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the comment object"""
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'user', 'page', 'content', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')