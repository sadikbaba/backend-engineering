from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class SessionLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        login(request, user)
        request.session.set_expiry(60 * 60)
        return Response({"message": "Login successfully"}, status=status.HTTP_200_OK)


class SessionLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successfully"}, status=status.HTTP_200_OK)


class SessionMeView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response(
                {
                    "authenticated": True,
                    "username": request.user.username,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"authenticated": False, "username": None}, status=status.HTTP_200_OK
        )


class SessionCsrfView(APIView):
    def get(self, request):
        csrf_token = get_token(request)

        return Response(
            {"csrfToken": csrf_token},
            status=status.HTTP_200_OK,
        )
