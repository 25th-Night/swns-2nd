from django.http import JsonResponse
from django.conf import settings


class CheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/health/":
            return JsonResponse({"status": "ok"})
        elif request.path == "/version/":
            return JsonResponse({"version": settings.VERSION})

        return self.get_response(request)
