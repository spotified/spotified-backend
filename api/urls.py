# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import include

app_name = "api"

urlpatterns = [
    url(r"auth/", include("users.urls")),
    url(r"playlists/", include("playlists.urls")),
]
