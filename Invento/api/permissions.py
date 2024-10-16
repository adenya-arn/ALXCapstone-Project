from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    Others can only read (GET).
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.creator == request.user  # Ensure the object has a `creator` field
