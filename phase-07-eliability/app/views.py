import hashlib
import json

from django.db import transaction, IntegrityError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import IdempotencyRecord, Order, Product
from .serializer import CreateOrderSerializer, OrderSerializer


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):

        idempotency_key = request.headers.get("Idempotency-Key")
        if not idempotency_key:
            return Response(
                {"error": "Idempotency-Key header is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        product = validated_data["product"]
        quantity = validated_data["quantity"]

        user = request.user

        payload_string = json.dumps(validated_data, sort_keys=True)
        payload_hash = hashlib.sha256(payload_string.encode("utf-8")).hexdigest()

        existing_record = IdempotencyRecord.objects.filter(
            user=user, operation="create_order", key=idempotency_key
        ).first()

        if existing_record:
            if existing_record.request_hash == payload_hash:
                return Response(
                    existing_record.response_body,
                    status=existing_record.response_status,
                )
            else:
                return Response(
                    {"error": "Idempotency key reused with different payload."},
                    status=status.HTTP_409_CONFLICT,
                )

        try:
            with transaction.atomic(), transaction.atomic():
                product_obj = Product.objects.select_for_update().get(pk=product.pk)

                if product_obj.stock < quantity:
                    return Response(
                        {"error": "Insufficient stock."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                product_obj.stock -= quantity
                product_obj.save()

                order = Order.objects.create(
                    user=user,
                    product=product_obj,
                    quantity=quantity,
                    # status PENDING by default
                )

                response_serializer = OrderSerializer(order)
                response_data = response_serializer.data
                response_status = status.HTTP_201_CREATED

                IdempotencyRecord.objects.create(
                    user=user,
                    operation="create_order",
                    key=idempotency_key,
                    request_hash=payload_hash,
                    response_status=response_status,
                    response_body=response_data,
                    order=order,
                )

                return Response(response_data, status=response_status)
        except IntegrityError:
            existing_record = IdempotencyRecord.objects.get(
                user=user, operation="create_order", key=idempotency_key
            )

            if existing_record.request_hash == payload_hash:
                return Response(
                    existing_record.response_body,
                    status=existing_record.response_status,
                )
            else:
                return Response(
                    {"error": "Idempotency key reused with different payload."},
                    status=status.HTTP_409_CONFLICT,
                )


class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, pk):
        with transaction.atomic():
            try:
                order = Order.objects.select_for_update().get(pk=pk, user=request.user)
            except Order.DoesNotExist:
                return Response(
                    {"error": "Order not found or unauthorized."},
                    status=status.HTTP_200_OK,
                )

            if order.status == "CANCELLED":
                return Response(
                    {"message": "Order is already cancelled."},
                    status=status.HTTP_200_OK,
                )

            if order.status != "PENDING":
                return Response(
                    {"error": f"Cannot cancel an order with status '{order.status}'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            product_obj = Product.objects.select_for_update().get(pk=order.product.pk)
            product_obj.stock += order.quantity
            product_obj.save(update_fields=["stock"])

            order.status = "CANCELLED"
            order.save(update_fields=["status"])

            return Response(
                {"message": "Order cancelled successfully and stock restored."},
                status=status.HTTP_200_OK,
            )
