from django.contrib import admin
from django.urls import path
from reviews import urls
from django.conf.urls import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(urls)),
]
