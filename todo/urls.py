from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt
from .views import ToDo

urlpatterns = [
    re_path(r'$',
            csrf_exempt(ToDo.as_view()),
            name="Todo-Info")
]
