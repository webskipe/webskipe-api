from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            # For published public pages, allow anyone to view
            if hasattr(obj, 'status') and hasattr(obj, 'privacy'):
                if obj.status == 'published' and obj.privacy == 'public':
                    return True
                # For unlisted pages, allow access via direct link
                if obj.status == 'published' and obj.privacy == 'unlisted':
                    return True
                # For private or draft pages, only allow the owner
                return obj.user == request.user
            return True
        
        # Write permissions are only allowed to the owner of the object
        return obj.user == request.user