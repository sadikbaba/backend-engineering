from django.http import JsonResponse
import requests


def weather_view(request):

    return JsonResponse({"message": "Weather API is working"}, status=200)
