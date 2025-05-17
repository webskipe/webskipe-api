from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'avatar')
        read_only_fields = ('id',)

class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a user"""
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        read_only_fields = ('id',)
    
    def create(self, validated_data):
        """Create a new user with encrypted password"""
        return User.objects.create_user(**validated_data)

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )