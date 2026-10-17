from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .jwt_views import JWTLogoutView, JWTMeView, JWTRegisterView
from .session_views import (
    SessionCsrfView,
    SessionLoginView,
    SessionLogoutView,
    SessionMeView,
)
from .token_views import TokenLoginView, TokenLogoutView, TokenMeView

urlpatterns = [
    path("session/login/", SessionLoginView.as_view()),
    path("session/logout/", SessionLogoutView.as_view()),
    path("session/me/", SessionMeView.as_view()),
    path("session/csrf/", SessionCsrfView.as_view()),
    # authtoken
    path("token/login/", TokenLoginView.as_view()),
    path("token/me/", TokenMeView.as_view()),
    path("token/logout/", TokenLogoutView.as_view()),
    # jwt
    path("jwt/login/", TokenObtainPairView.as_view()),
    path("jwt/me/", JWTMeView.as_view()),
    path("jwt/refresh/", TokenRefreshView.as_view()),
    path("jwt/register/", JWTRegisterView.as_view()),
    path("jwt/logout/", JWTLogoutView.as_view()),
]


# {
#   "username": "sadiktest",
#   "password": "test12345"
# }
