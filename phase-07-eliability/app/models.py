from django.conf import settings
from django.db import models
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=150)
    stock = models.PositiveIntegerField()


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="orders"
    )
    quantity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [  # noqa: RUF012
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0),  # Django 5.1+
                name="order_quantity_gt_0",
            ),
        ]


class IdempotencyRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="idempotency_records",
    )
    operation = models.CharField(max_length=100)  # e.g. "create_order"
    key = models.CharField(max_length=255)
    request_hash = models.CharField(max_length=64)  # sha256 hex
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name="idempotency_records",
        null=True,
        blank=True,
    )
    response_status = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    response_body = models.JSONField(
        null=True,
        blank=True,
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(
                fields=["user", "operation", "key"],
                name="uniq_user_operation_key",
            ),
        ]
