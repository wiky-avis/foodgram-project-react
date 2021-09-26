from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated


class GetPost(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.method == 'POST':
            return True
        return super().has_permission(request, view)


class CurrentUserOrAdmin(AllowAny):
    def has_object_permission(self, request, view, obj):
        return (request.user.is_staff
                or request.user == obj.author
                or request.method in SAFE_METHODS)
