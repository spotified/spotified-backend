from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from spotipy import SpotifyException
from utils.spotify import spotify_uri_or_link_to_id

from . import serializers as se
from .models import Artist, Playlist, PlaylistTrack, PlaylistTrackVote, Track


class PlaylistView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, playlist_id=None):
        if playlist_id:
            playlist_obj = get_object_or_404(Playlist, pk=playlist_id)
            playlist = se.PlaylistSerializer(instance=playlist_obj)
            return Response(playlist.data)
        else:
            playlist_qs = Playlist.objects.all()
            playlists = se.PlaylistOverviewSerializer(playlist_qs, many=True)
            return Response(playlists.data)

    def post(self, request):
        request.data["owner"] = request.user.pk
        playlist = se.PlaylistSerializer(data=request.data)

        if playlist.is_valid(raise_exception=True):
            playlist.save()
            return Response(playlist.data, status=status.HTTP_201_CREATED)


class PlaylistTrackView(APIView):
    @transaction.atomic()
    def post(self, request, playlist_id):
        playlist_obj = get_object_or_404(Playlist, pk=playlist_id)
        track_spotify_id = spotify_uri_or_link_to_id(
            request.data.get("spotify_id"), content_type="track"
        )

        try:
            track_obj = Track.objects.get(spotify_id=track_spotify_id)
        except Track.DoesNotExist:
            # fetch track info
            try:
                track_info = request.user.spotify_api.track(track_spotify_id)
            except SpotifyException:
                raise ValidationError({"spotify_id": _("Track unknown")})

            if track_info.get("is_local"):
                raise ValidationError(
                    {"spotify_id": _("Track is local thus can't be added")}
                )

            # save artists
            track_info_artists = track_info["album"].get("artists", [])
            artists = []
            for track_info_artist in track_info_artists:
                try:
                    artists.append(
                        Artist.objects.get(spotify_id=track_info_artist["id"])
                    )
                except Artist.DoesNotExist:
                    artist = se.ArtistSerializer(
                        data={
                            "spotify_id": track_info_artist["id"],
                            "name": track_info_artist["name"],
                        }
                    )
                    if artist.is_valid(raise_exception=True):
                        artist.save()
                        artists.append(artist.instance)

            track = se.TrackSerializer(
                data={"spotify_id": track_info["id"], "name": track_info["name"]}
            )

            if track.is_valid(raise_exception=True):
                track.save(artists=artists)

            track_obj = track.instance

        # save playlist <-> track relation
        playlist_track_obj, created = PlaylistTrack.objects.get_or_create(
            playlist=playlist_obj, track=track_obj
        )

        if not created:
            raise ValidationError(
                {"spotify_id": _("The track is already included in this playlist")}
            )

        return Response({})


class PlaylistTrackVoteView(APIView):
    def post(self, request, playlist_id, track_id, up_or_down):
        playlist_obj = get_object_or_404(Playlist, pk=playlist_id)
        track_obj = get_object_or_404(Track, pk=track_id)
        playlist_track_obj = PlaylistTrack.objects.get(
            playlist=playlist_obj, track=track_obj
        )

        if up_or_down == "up":
            up_or_down = PlaylistTrackVote.VOTE_UP
        else:
            up_or_down = PlaylistTrackVote.VOTE_DOWN

        try:
            playlist_track_vote_obj = PlaylistTrackVote.objects.get(
                voter=request.user, playlist_track=playlist_track_obj
            )
            playlist_track_vote_obj.vote = up_or_down
            playlist_track_vote_obj.save()
        except PlaylistTrackVote.DoesNotExist:
            playlist_track_vote = se.PlaylistTrackVoteSerializer(
                data={
                    "voter": request.user.pk,
                    "playlist_track": playlist_track_obj.pk,
                    "vote": up_or_down,
                }
            )

            if playlist_track_vote.is_valid(raise_exception=True):
                playlist_track_vote.save()

        # recalculate the score
        playlist_track_obj.save()

        return Response({})
