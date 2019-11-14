from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt
from .views import ToDo, Bucket

urlpatterns = [
    re_path(r'todos$',
            csrf_exempt(ToDo.as_view()),
            name="Todos"),
    re_path(r'todos/(?P<id>\d+)$',
            csrf_exempt(ToDo.as_view()),
            name="Todo"),
    re_path(r'buckets$',
            csrf_exempt(Bucket.as_view()),
            name="Buckets"),
]
