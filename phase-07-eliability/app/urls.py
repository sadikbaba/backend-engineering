from django.urls import path

from .views import CreateOrderView, CancelOrderView, ProductView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("order/", CreateOrderView.as_view()),
    path("order/<int:pk>/cancel/", CancelOrderView.as_view()),
    path("products/", ProductView.as_view(), name="product-list"),
    path("login/", TokenObtainPairView.as_view()),
]
