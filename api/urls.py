# -*- coding: utf-8 -*-
from django.urls import include, path

app_name = "api_v1"

urlpatterns = [
    path("auth/", include("users.urls")),
    path("playlists/", include("playlists.urls")),
]
