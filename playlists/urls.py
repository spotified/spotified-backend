from django.urls import path

from . import views

app_name = "playlists"

urlpatterns = [
    path("", views.PlaylistView.as_view(), name="playlists"),
    path(
        "<int:playlist_id>/tracks/",
        views.PlaylistTrackView.as_view(),
        name="playlist_track",
    ),
]
