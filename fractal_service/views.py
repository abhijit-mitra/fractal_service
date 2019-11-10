from django.views import View
from django.http.response import JsonResponse


class HealthCheck(View):
    def get(self, *args, **kwargs):
        return JsonResponse(data='Service is up', status=200, safe=False)
