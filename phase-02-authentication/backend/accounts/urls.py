from django.urls import path

from .session_views import SessionLoginView, SessionLogoutView, SessionMeView

urlpatterns = [
    path("session/login/", SessionLoginView.as_view()),
    path("session/logout/", SessionLogoutView.as_view()),
    path("session/me/", SessionMeView.as_view()),
]
