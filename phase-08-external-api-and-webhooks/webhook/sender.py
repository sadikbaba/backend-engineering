import hashlib
import hmac
import json

import requests

secret = b"learning-secret"
event = {"event": "payment.success", "payment_id": "pay_123", "amount": 5000}


raw_body = json.dumps(event).encode("utf-8")
sig = hmac.new(secret, raw_body, digestmod=hashlib.sha256).hexdigest()

url = "http://127.0.0.1:8000/api/"

response = requests.post(
    url,
    data=raw_body,
    headers={
        "Content-Type": "application/json",
        "X-Webhook-Signature": sig,
    },
)

print(response.status_code)
print(response.text)
