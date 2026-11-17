from rest_framework import serializers

from .models import Product, Order


class CreateOrderSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [  # noqa: RUF012
            "id",
            "user",
            "product",
            "quantity",
            "status",
            "created_at",
        ]

        read_only_fields = ["id", "user", "status", "created_at"]  # noqa: RUF012
