import math  # noqa: I001

import requests
from django.http import JsonResponse
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


def weather_view(request):
    latitude_raw = request.GET.get("latitude")
    longitude_raw = request.GET.get("longitude")

    if not latitude_raw or not longitude_raw:
        return JsonResponse(
            {"error": "Both latitude and longitude query parameters are required."},
            status=400,
        )

    try:
        latitude = float(latitude_raw)
        longitude = float(longitude_raw)
    except ValueError:
        return JsonResponse(
            {"error": "Latitude and longitude must be valid numbers."},
            status=400,
        )

    if not (math.isfinite(latitude) and math.isfinite(longitude)):
        return JsonResponse(
            {"error": "Latitude and longitude must be finite numbers."},
            status=400,
        )

    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        return JsonResponse(
            {
                "error": "Latitude must be between -90 and 90, and longitude must be between -180 and 180."
            },
            status=400,
        )

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    }

    retry_policy = Retry(
        connect=3,
        total=3,
        backoff_factor=1,
        status_forcelist=[502, 503, 504],
        allowed_methods={"GET"},
    )
    adapter = HTTPAdapter(max_retries=retry_policy)
    session = requests.Session()
    session.mount("https://", adapter)

    try:
        response = session.get(
            "https://api.open-meteo.com/v1/forecast", params=params, timeout=10
        )

        response.raise_for_status()
        data = response.json()
    except requests.Timeout:
        return JsonResponse({"error": "Weather service timed out."}, status=504)
    except requests.RequestException:
        return JsonResponse({"error": "Weather service unavailable."}, status=502)
    except ValueError:
        return JsonResponse(
            {"error": "Invalid response from weather service."}, status=502
        )

    current = data["current"]
    units = data["current_units"]

    result = {
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "temperature": current["temperature_2m"],
        "temperature_unit": units["temperature_2m"],
        "relative_humidity": current["relative_humidity_2m"],
        "relative_humidity_unit": units["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "wind_speed_unit": units["wind_speed_10m"],
    }

    return JsonResponse(result, status=200)
