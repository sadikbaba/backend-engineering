from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .jwt_views import JWTLogoutView, JWTMeView, JWTRegisterView
from .role_views import AssignRoleView, RemoveRoleView

urlpatterns = [
    # jwt
    path("jwt/login/", TokenObtainPairView.as_view()),
    path("jwt/me/", JWTMeView.as_view()),
    path("jwt/refresh/", TokenRefreshView.as_view()),
    path("jwt/register/", JWTRegisterView.as_view()),
    path("jwt/logout/", JWTLogoutView.as_view()),
    # roles
    path("roles/assign/", AssignRoleView.as_view()),
    path("roles/remove/", RemoveRoleView.as_view()),
]
