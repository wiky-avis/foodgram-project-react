from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin


class IsSuperuser(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and request.user.is_superuser)


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and obj.author == request.user)


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user == obj.author


class IsAuthorOrAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif (request.method in ('POST',) and request.user.is_authenticated):
            return True
        elif (request.method in ('PUT', 'PATCH', 'DELETE')
              and request.user.is_authenticated
              and (request.user == obj.author or request.user.is_admin)):
            return True
        return False
