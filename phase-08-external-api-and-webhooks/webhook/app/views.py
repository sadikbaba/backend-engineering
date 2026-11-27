import hashlib
import hmac
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

WEBHOOK_SECRET = b"learning-secret"


@csrf_exempt
@require_POST
def receive_webhook(request):

    received_signature = request.headers.get("X-Webhook-Signature")

    if not received_signature:
        return JsonResponse(
            {"error": "Missing signature"},
            status=401,
        )

    expected_signature = hmac.new(
        WEBHOOK_SECRET, request.body, digestmod=hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, received_signature):
        return JsonResponse(
            {"error": "Invalid signature"},
            status=401,
        )

    try:
        event = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    if not isinstance(event, dict):
        return JsonResponse({"error": "Invalid event structure"}, status=400)

    required_fields = ("event", "payment_id", "amount")

    if not all(field in event for field in required_fields):
        return JsonResponse({"error": "Missing required fields"}, status=400)

    payment_id = event.get("payment_id")
    amount = event.get("amount")
    event_type = event.get("event")

    if not isinstance(payment_id, str) or not payment_id.strip():
        return JsonResponse({"error": "Invalid payment_id"}, status=400)

    if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
        return JsonResponse({"error": "Invalid amount"}, status=400)

    if not isinstance(event_type, str) or not event_type.strip():
        return JsonResponse({"error": "Unsupported event type"}, status=400)

    return JsonResponse({"message": "Signature verified"}, status=200)
