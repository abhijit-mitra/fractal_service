from django.contrib import admin
from django.urls import re_path
from django.conf.urls import include
from .views import HealthCheck

admin.autodiscover()

urlpatterns = [
    re_path(r'$', HealthCheck.as_view()),
    re_path(r'admin/', admin.site.urls),
    re_path(r'todo/', include('todo.urls')),
]
