from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Пермишен для админа.
    """
    def has_permission(self, request, view):
        return (request.user.role == 'admin', request.user.is_authenticated)
    def has_object_permission(self, request, view, obj):
        return (request.user.role == 'admin', request.user.is_authenticated)

class IsModerator(permissions.BasePermission):
    """
    Пермишен для модератора.
    """
    def has_permission(self, request, view):
        return (request.user.role == 'moderator', request.user.is_authenticated)
    def has_object_permission(self, request, view, obj):
        return (request.user.role == 'moderator', request.user.is_authenticated)

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


class IsAuthOrReadOnly(permissions.BasePermission):
    """Проверяет, что пользователь залогинен и он - автор записи."""

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




