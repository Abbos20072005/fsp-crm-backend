from rest_framework.permissions import BasePermission


class IsSuperAdminOrHR(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role in [3, 4]:
            return True
        return False


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role not in [1, 2, 3, 4]:
            return True
        return False