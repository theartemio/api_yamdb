from rest_framework import permissions 


class IsAuthorOrStaff(permissions.BasePermission):
    """
    Кастомный пермишен, разрешающий доступ только авторам объекта,
    модераторам или администраторам.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        return obj.author == request.user or request.user.is_staff

# Работает
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