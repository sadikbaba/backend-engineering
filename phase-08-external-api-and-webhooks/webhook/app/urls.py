from django.urls import path
from .views import receive_webhook

urlpatterns = [
    path("", receive_webhook),
]
