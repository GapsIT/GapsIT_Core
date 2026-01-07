from rest_framework import permissions
from django.conf import settings


class IsAdmin(permissions.BasePermission):
    """Check if user is admin via employee role or Django staff status"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Check Django admin status
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Check employee admin role
        try:
            return request.user.employee.is_admin
        except:
            return False


class IsOwnerOrAdmin(permissions.BasePermission):
    """Allow access to own employee record or if admin"""

    def has_object_permission(self, request, view, obj):
        # Admins can access any employee
        if request.user.is_staff or request.user.is_superuser:
            return True

        try:
            if request.user.employee.is_admin:
                return True
        except:
            pass

        # Employees can only access their own record
        return obj.user == request.user


class HasAdminAPIKey(permissions.BasePermission):
    """Check for valid admin API key in request headers"""

    def has_permission(self, request, view):
        api_key = request.headers.get("X-API-Key")
        if api_key and api_key == settings.ADMIN_API_KEY:
            return True
        return False
