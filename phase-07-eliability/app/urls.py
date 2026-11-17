from django.urls import path

from .views import CreateOrderView, CancelOrderView

urlpatterns = [
    path("order/", CreateOrderView.as_view()),
    path("order/<int:pk>/cancel/", CancelOrderView.as_view()),
]
