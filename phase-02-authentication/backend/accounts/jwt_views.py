from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer


class JWTMeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):

        return Response(
            {
                "authenticated": True,
                "username": request.user.username,
            }
        )


class JWTRegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User registered successfully",
                    "username": serializer.data["username"],
                },
                status=201,
            )
        return Response(serializer.errors, status=400)


class JWTLogoutView(APIView):
    def post(self, request):

        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({
                    "message" : "Refresh token is required"
                },status=400)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message" : "Logout successfully"}, status=200)
        except TokenError as error:
            return Response({
                "message" : str(error)
            }, status=400)