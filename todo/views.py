from django.views import View
from django.http.response import JsonResponse
from .models import ToDOs


class ToDo(View):
    def get(self, *args, **kwargs):
        all_todos = list(ToDOs.objects.all().values('id', 'name', 'bucket__id', 'bucket__name'))
        return JsonResponse(data=all_todos, status=200, safe=False)
