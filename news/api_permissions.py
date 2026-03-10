from rest_framework import permissions


class IsJournalist(permissions.BasePermission):
    """
    Allow only journalist users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "journalist"


class IsEditor(permissions.BasePermission):
    """
    Allow only editor users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "editor"


class IsReader(permissions.BasePermission):
    """
    Allow only reader users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "reader"


class IsOwnerOrEditor(permissions.BasePermission):
    """
    Allow owner or editor users.
    """

    def has_object_permission(self, request, view, obj):
        # Editors or owner (journalist) can edit/delete
        if request.user.role == "editor":
            return True
        if hasattr(obj, "author") and obj.author and obj.author.user == request.user:
            return True
        return False
