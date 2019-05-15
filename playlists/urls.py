from django.urls import path, re_path

from . import views

app_name = "playlists"

urlpatterns = [
    path("", views.PlaylistView.as_view(), name="playlists"),
    path("<int:playlist_id>/", views.PlaylistView.as_view(), name="playlist"),
    path(
        "<int:playlist_id>/tracks/",
        views.PlaylistTrackView.as_view(),
        name="playlist_track",
    ),
    path(
        "<int:playlist_id>/tags/",
        views.PlaylistTagsView.as_view(),
        name="playlist_tags",
    ),
    path(
        "<int:playlist_id>/tags/<int:tag_id>/",
        views.PlaylistTagsView.as_view(),
        name="playlist_tag",
    ),
    re_path(
        r"(?P<playlist_id>\d+)/tracks/(?P<track_id>\d+)/vote/(?P<up_or_down>(up|down))/",
        views.PlaylistTrackVoteView.as_view(),
        name="playlist_track_vote",
    ),
]
