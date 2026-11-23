from rest_framework import serializers

from .models import Order, Product


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


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"  # or list specific fields like ["id", "name", "price"]
