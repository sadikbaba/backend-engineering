from django.contrib.auth.models import Group, User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import IsAppAdmin


class AssignRoleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAppAdmin]

    def post(self, request):
        username = request.data.get("username")
        role_name = request.data.get("role")

        allowed_roles = {"viewer", "editor", "admin"}

        if not username or not role_name:
            return Response(
                {"detail": "username and role are required."},
                status=400,
            )

        if role_name not in allowed_roles:
            return Response(
                {"detail": "Invalid role."},
                status=400,
            )
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"detail": "User does not exist."},
                status=404,
            )
        role = Group.objects.get(name=role_name)

        if (
            target_user == request.user
            and not request.user.is_superuser
            and role_name != "admin"
        ):
            return Response(
                {"detail": "You cannot remove your own admin role."},
                status=400,
            )

        target_user.groups.set([role])

        return Response(
            {"detail": "User role updated."},
            status=200,
        )


class RemoveRoleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAppAdmin]

    def post(self, request):
        username = request.data.get("username")
        role_name = request.data.get("role")

        allowed_roles = {"viewer", "editor", "admin"}

        if not username or not role_name:
            return Response(
                {"detail": "username and role are required."},
                status=400,
            )

        if role_name not in allowed_roles:
            return Response(
                {"detail": "Invalid role."},
                status=400,
            )
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"detail": "User does not exist."},
                status=404,
            )
        role = Group.objects.get(name=role_name)

        if (
            target_user == request.user
            and not request.user.is_superuser
            and role_name == "admin"
        ):
            return Response(
                {"detail": "You cannot remove your own admin role."},
                status=400,
            )

        target_user.groups.remove(role)

        return Response(
           {"detail":"User role updated."},
            status=200,
        )