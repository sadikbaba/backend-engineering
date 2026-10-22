from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        # roles
        viewer, _ = Group.objects.get_or_create(name="viewer")
        editor, _ = Group.objects.get_or_create(name="editor")
        admin, _ = Group.objects.get_or_create(name="admin")

        # Permissions
        view_note = Permission.objects.get(
            codename="view_note",
            content_type__app_label="notes",
        )
        change_note = Permission.objects.get(
            codename="change_note",
            content_type__app_label="notes",
        )
        add_note = Permission.objects.get(
            codename="add_note",
            content_type__app_label="notes",
        )
        delete_note = Permission.objects.get(
            codename="delete_note",
            content_type__app_label="notes",
        )

        viewer.permissions.set([view_note])
        editor.permissions.set(
            [
                view_note,
                change_note,
                add_note,
                delete_note,
            ]
        )

        admin.permissions.set(
            [
                view_note,
                change_note,
                add_note,
                delete_note,
            ]
        )
