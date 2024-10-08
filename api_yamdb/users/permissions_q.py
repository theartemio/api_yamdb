from rest_framework import permissions



class IsAdmin(permissions.BasePermission):
    """
    Пермишен для админа.
    """
    def has_permission(self, request, view):
        return request.user.role == 'admin' and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' and request.user.is_authenticated
