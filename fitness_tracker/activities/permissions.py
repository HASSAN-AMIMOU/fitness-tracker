
from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Only allow the owner of an object to access it
        return obj.user == request.user