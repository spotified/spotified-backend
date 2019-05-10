import spotipy
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from spotipy import SpotifyException

from .serializers import PlaylistSerializer


class PlayList(APIView):
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        user = request.user

        request.data["owner"] = user.pk
        playlist = PlaylistSerializer(data=request.data)
        playlist.owner = user

        try:
            if playlist.is_valid(raise_exception=True):
                sp = spotipy.Spotify(auth=user.access_token)
                sp.user_playlist_create(
                    user.spotify_id, request.data["name"], public=True
                )
                playlist.save()
                return Response({})
        except SpotifyException as e:
            return Response(str(e))
