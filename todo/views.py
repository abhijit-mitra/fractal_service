from django.views import View
from django.http.response import JsonResponse


class ToDo(View):
    def get(self, *args, **kwargs):
        return JsonResponse(data=[], status=200, safe=False)
