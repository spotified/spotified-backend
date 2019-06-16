from django.db import transaction
from django.db.models import F
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from spotipy import SpotifyException
from users.mixins import AuthTokenExpiresAtHeaderMixin
from utils.spotify import spotify_uri_or_link_to_id

from . import models as m
from . import serializers as se


class PlaylistView(AuthTokenExpiresAtHeaderMixin):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, playlist_id=None):
        if playlist_id:
            playlist_obj = get_object_or_404(m.Playlist, pk=playlist_id)
            playlist = se.PlaylistReadSerializer(instance=playlist_obj)
            return Response(playlist.data)
        else:
            playlist_qs = m.Playlist.objects.all()
            playlists = se.PlaylistReadSerializer(playlist_qs, many=True)
            return Response(playlists.data)

    def post(self, request):
        playlist = se.PlaylistWriteSerializer(
            data={**request.data, **{"owner": request.user.pk}}
        )

        if playlist.is_valid(raise_exception=True):
            # create Playlist at Spotify
            create_response = request.user.spotify_api.user_playlist_create(
                request.user.spotify_id,
                "{}".format(playlist.validated_data["name"]),
                public=True,
            )

            # save the playlist
            playlist.save(
                spotify_id=create_response["id"],
                spotify_snapshot_id=create_response["snapshot_id"],
            )

            return Response(playlist.data)


class PlaylistTrackView(AuthTokenExpiresAtHeaderMixin):
    @transaction.atomic()
    def post(self, request, playlist_id):
        playlist_obj = get_object_or_404(m.Playlist, pk=playlist_id)
        track_spotify_id = spotify_uri_or_link_to_id(
            request.data.get("spotify_id"), content_type="track"
        )

        try:
            track_obj = m.Track.objects.get(spotify_id=track_spotify_id)
        except m.Track.DoesNotExist:
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
                        m.Artist.objects.get(spotify_id=track_info_artist["id"])
                    )
                except m.Artist.DoesNotExist:
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
        playlist_track_obj, created = m.PlaylistTrack.objects.get_or_create(
            playlist=playlist_obj, track=track_obj, added_by=request.user
        )

        if not created:
            raise ValidationError(
                {"spotify_id": _("The track is already included in this playlist")}
            )

        return Response({})


class PlaylistTrackVoteView(AuthTokenExpiresAtHeaderMixin):
    def post(self, request, playlist_id, track_id, up_or_down):
        playlist_obj = get_object_or_404(m.Playlist, pk=playlist_id)
        track_obj = get_object_or_404(m.Track, pk=track_id)
        playlist_track_obj = m.PlaylistTrack.objects.get(
            playlist=playlist_obj, track=track_obj
        )

        if up_or_down == "up":
            up_or_down = m.PlaylistTrackVote.VOTE_UP
        else:
            up_or_down = m.PlaylistTrackVote.VOTE_DOWN

        try:
            playlist_track_vote_obj = m.PlaylistTrackVote.objects.get(
                voter=request.user, playlist_track=playlist_track_obj
            )
            playlist_track_vote_obj.vote = up_or_down
            playlist_track_vote_obj.save()
        except m.PlaylistTrackVote.DoesNotExist:
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


class PlaylistTagsView(AuthTokenExpiresAtHeaderMixin):
    @transaction.atomic()
    def post(self, request, playlist_id):
        playlist_obj = get_object_or_404(m.Playlist, pk=playlist_id)

        tag = se.PlaylistTagSerializer(data=request.data)

        if tag.is_valid(raise_exception=True):
            tag.save()

            if not playlist_obj.tags.filter(pk=tag.instance.pk).count():
                tag.instance.count = F("count") + 1
                tag.instance.save()
                playlist_obj.tags.add(tag.instance)

        return Response(tag.data)

    @transaction.atomic()
    def delete(self, request, playlist_id, tag_id):
        playlist_obj = get_object_or_404(m.Playlist, pk=playlist_id)
        tag_obj = get_object_or_404(
            m.PlaylistTag.objects.select_for_update(), pk=tag_id
        )

        playlist_obj.tags.filter(pk=tag_obj.pk).delete()
        tag_obj.count = tag_obj.count - 1
        tag_obj.save()

        return Response({})


class TagView(AuthTokenExpiresAtHeaderMixin):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        name = self.request.query_params.get("name", "")
        tag_objs = m.PlaylistTag.objects.filter(name__startswith=name).order_by(
            "-count"
        )[0:50]
        tags = se.PlaylistTagSerializer(instance=tag_objs, many=True)
        return Response(tags.data)
