from django.views import View
from django.http.response import JsonResponse
from .models import Buckets


class ToDo(View):
    def get(self, *args, **kwargs):
        all_buckets = list(Buckets.objects.all().values('id', 'name'))
        return JsonResponse(data=all_buckets, status=200, safe=False)
