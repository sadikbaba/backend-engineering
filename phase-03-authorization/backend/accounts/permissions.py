from rest_framework.permissions import BasePermission


class IsAppAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.groups.filter(name="admin").exists()
        )
