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
            if request.user.is_superuser:
                return True
            if request.user.role == 'admin':
                return True
            return False
    def has_object_permission(self, request, view, obj):
        return True
        # return request.user.role == 'admin'
