from rest_framework import permissions


class Admin(permissions.BasePermission):

    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            if request.user.role == 'admin':
                return True
            return False
        # return (request.user.role == 'admin', request.user.is_aithenticated)


class Moderator(permissions.BasePermission):

    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            if request.user.role == 'moderator':
                return True
            return False
        # return (request.user.role == 'moderator', request.user.is_aithenticated)


class Userr(permissions.BasePermission):

    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            if request.user.role == 'user':
                return True
            return False
        # return (request.user.role == 'user', request.user.is_aithenticated)
