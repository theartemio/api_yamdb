from rest_framework.permissions import BasePermission


class IsAuthorOrStaff(BasePermission):
    """
    Кастомный пермишен, разрешающий доступ только авторам объекта,
    модераторам или администраторам.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        return obj.author == request.user or request.user.is_staff
