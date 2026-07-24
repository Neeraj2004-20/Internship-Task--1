from django.contrib import admin
from django.urls import path
from movies.views import movie_discovery_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", movie_discovery_view, name="movie-discovery"),
]
