from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("username", type=str)
        parser.add_argument("role", type=str)

    def handle(self, *args, **options):
        username = options["username"]
        role_name = options["role"]

        user = User.objects.get(username=username)
        role = Group.objects.get(name=role_name)

        user.groups.set([role])

        self.stdout.write(
            self.style.SUCCESS(f"{username} assigned to role {role_name}")
        )
