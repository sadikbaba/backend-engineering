from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Purchase


class PurchaseView(APIView):
    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            return Response(
                {"message": "Quantity must be a positive integer"}, status=400
            )
        if (
            not isinstance(product_id, int)
            or isinstance(product_id, bool)
            or product_id <= 0
        ):
            return Response(
                {"message": "Product id must be a positive integer"}, status=400
            )

        with transaction.atomic():
            try:
                product = Product.objects.select_for_update().get(id=product_id)
            except Product.DoesNotExist:
                return Response({"message": "Product not found"}, status=404)

            if product.stock >= quantity:
                updated_stock = product.stock - quantity
                product.stock = updated_stock
                product.save(update_fields=["stock"])
                Purchase.objects.create(product=product, quantity=quantity)

                return Response({"message": "purchase successful"}, status=200)

        return Response({"message": "no available stock "}, status=400)
