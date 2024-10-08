from rest_framework import permissions


class IsSuperUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsAdmin(permissions.BasePermission):
    """
    Пермишен для админа.
    """
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            if request.user.role == 'admin':
                return True
            return False
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' and request.user.is_authenticated

class IsAdminOrReadonly(permissions.BasePermission):
    """
    Пермишен для админа.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.role == 'admin'
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.role == 'admin'
        )

class IsModeratorOrAdmin(permissions.BasePermission):
    """
    Permission that allows moderators and admins to edit and delete any content.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in ['moderator', 'admin']

class IsModerator(permissions.BasePermission):
    """
    Пермишен для модератора.
    """
    roles = ('admin', 'moderator')
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.role == 'moderator'
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.role == 'moderator'
        )

class IsUser(permissions.BasePermission):
    """
    Пермишен для проверки аутентифицированных пользователей.
    
    Проверяет что пользователь:
     - залогинен, тогда он может читать и просматривать все,
     - является автором записи, тогда он может ее менять

    Анонимный пользователь может выполнять безопасные запросы,
    просматривать весь контент.
    """

    def has_permission(self, request, view):

        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Проверяет, что пользователь залогинен и он - автор записи."""

    def has_permission(self, request, view):
        # Safe methods are always allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the author of the review/comment.
        return obj.author == request.user


