from rest_framework import permissions


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action in ["update", "partial_update", "destroy"]:
            if obj.owner == request.user:
                return True
            if view.action == "destroy" and request.user.is_staff:
                return True

        return False


class IsCommentOwnerOrPostOwnerOrAdminOrGetMethod(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if view.action == "update":
            return obj.user == request.user
        if view.action == "destroy":
            return (
                obj.user == request.user
                or obj.post.owner == request.user
                or request.user.is_staff
            )
