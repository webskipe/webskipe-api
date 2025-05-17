from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Page, PageMedia

class PageMediaSerializer(serializers.ModelSerializer):
    """Serializer for page media"""
    
    class Meta:
        model = PageMedia
        fields = ('id', 'file', 'file_type', 'created_at')
        read_only_fields = ('id', 'created_at')

class PageSerializer(serializers.ModelSerializer):
    """Serializer for pages"""
    
    media = PageMediaSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    view_url = serializers.SerializerMethodField()
    reactions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Page
        fields = (
            'id', 'user', 'title', 'slug', 'context', 'message', 'tone',
            'template', 'primary_color', 'background_color', 'privacy',
            'status', 'expiry_date', 'views', 'created_at', 'updated_at',
            'media', 'view_url', 'reactions_count'
        )
        read_only_fields = ('id', 'slug', 'views', 'created_at', 'updated_at')
    
    def get_view_url(self, obj):
        return f"/view/{obj.slug}"
    
    def get_reactions_count(self, obj):
        return obj.reactions.count()
    
    def create(self, validated_data):
        """Create a page with current user"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class PageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new page"""
    
    class Meta:
        model = Page
        fields = (
            'title', 'context', 'message', 'tone', 'template',
            'primary_color', 'background_color', 'privacy',
            'status', 'expiry_date'
        )
    
    def create(self, validated_data):
        """Create a page with current user"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class PageListSerializer(serializers.ModelSerializer):
    """Serializer for listing pages (with less fields)"""
    
    user = UserSerializer(read_only=True)
    reactions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Page
        fields = (
            'id', 'user', 'title', 'slug', 'tone', 'template',
            'privacy', 'status', 'views', 'created_at',
            'reactions_count'
        )
    
    def get_reactions_count(self, obj):
        return obj.reactions.count()