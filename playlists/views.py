from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from spotipy import SpotifyException
from utils.spotify import spotify_uri_or_link_to_id

from .models import Artist, Playlist, PlaylistTracks, Track
from .serializers import ArtistSerializer, PlaylistSerializer, TrackSerializer


class PlaylistView(APIView):
    def post(self, request, *args, **kwargs):
        request.data["owner"] = request.user.pk
        playlist = PlaylistSerializer(data=request.data)

        if playlist.is_valid(raise_exception=True):
            playlist.save()
            return Response(playlist.data, status=status.HTTP_201_CREATED)


class PlaylistTrackView(APIView):
    @transaction.atomic()
    def post(self, request, playlist_id, *args, **kwargs):
        playlist_obj = get_object_or_404(Playlist, pk=playlist_id)
        track_spotify_id = spotify_uri_or_link_to_id(request.data.get("spotify_id"))

        try:
            track_obj = Track.objects.get(spotify_id=track_spotify_id)
        except Track.DoesNotExist:
            # fetch Song info
            try:
                track_info = request.user.spotify_api.track(track_spotify_id)
            except SpotifyException:
                raise ValidationError({"spotify_id": _("Track unknown.")})

            if track_info.get("is_local"):
                raise ValidationError(
                    {"spotify_id": _("Track is local thus can't be added.")}
                )

            track = TrackSerializer(
                data={"spotify_id": track_info["id"], "name": track_info["name"]}
            )

            if track.is_valid(raise_exception=True):
                track.save()

            track_info_artists = track_info["album"].get("artists", [])
            for track_info_artist in track_info_artists:
                try:
                    artist_obj = Artist.objects.get(spotify_id=track_info_artist["id"])
                except Artist.DoesNotExist:
                    artist = ArtistSerializer(
                        data={
                            "spotify_id": track_info_artist["id"],
                            "name": track_info_artist["name"],
                        }
                    )
                    if artist.is_valid(raise_exception=True):
                        artist.save()
                        artist_obj = artist.instance

                track.instance.artists.add(artist_obj)
                track_obj = track.instance

        PlaylistTracks.objects.get_or_create(playlist=playlist_obj, track=track_obj)
        return Response({})
