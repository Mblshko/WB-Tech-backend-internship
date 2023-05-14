from rest_framework import permissions


class IsAdminOrAuthor(permissions.BasePermission):
    '''GET запросы всем пользователям. POST запросы только авторизованным. PUT и DELETE только авторам или админу.'''

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user or bool(request.user and request.user.is_staff)