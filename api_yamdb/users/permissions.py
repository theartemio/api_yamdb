from rest_framework import permissions


class IsAuthOrReadOnly(permissions.BasePermission):
    """
    Проверяет, что:
     - пользователь залогинен и он - автор записи. Если нет, то запись
     доступна только для чтения.
     - пользователь является админом или модером. Если да, то запись
     доступна для удаления и редактирования.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
            or request.user.is_superuser
        )


class IsAdminOrRestricted(permissions.BasePermission):
    """
    Пермишен для админа, обеспечивает доступ только админу.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.is_admin or request.user.is_superuser
        return False


class IsAdminOrReadonly(permissions.BasePermission):
    """
    Пермишен для админа, обеспечивает доступ для
    изменения только админу, остальным ролям и анонимным
    пользователям -
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
            or request.user.is_authenticated and request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
            or request.user.is_authenticated and request.user.is_superuser
        )
