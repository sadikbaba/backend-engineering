from django.urls import path

from .session_views import (
    SessionCsrfView,
    SessionLoginView,
    SessionLogoutView,
    SessionMeView,
)
from .token_views import TokenLoginView, TokenMeView

urlpatterns = [
    path("session/login/", SessionLoginView.as_view()),
    path("session/logout/", SessionLogoutView.as_view()),
    path("session/me/", SessionMeView.as_view()),
    path("session/csrf/", SessionCsrfView.as_view()),
    # authtoken
    path("token/login/", TokenLoginView.as_view()),
    path("token/me/", TokenMeView.as_view()),
]



# {
#   "username": "sadiktest",
#   "password": "test12345"
# }