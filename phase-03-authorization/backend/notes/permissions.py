from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    DjangoModelPermissions,
)


class NoteModelPermissions(DjangoModelPermissions):
    perms_map = {  # noqa: RUF012
        **DjangoModelPermissions.perms_map,  # copy all existing DRF rules first, then replace GET, HEAD, OPTIONS with our own rules
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "HEAD": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": ["%(app_label)s.view_%(model_name)s"],
    }


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        if request.user.groups.filter(name="admin").exists():
            return True

        return obj.owner == request.user
