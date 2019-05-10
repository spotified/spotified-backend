import spotipy
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from spotipy.oauth2 import SpotifyOauthError

from .models import SpotifyUser


class OAuthFlowStart(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        return Response({"url": SpotifyUser.oauth.get_authorize_url()})


class OAuthFlowFinish(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        auth_code = request.data.get("code")

        try:
            token_info = SpotifyUser.oauth.get_access_token(auth_code)

            # fetch profile info
            sp = spotipy.Spotify(auth=token_info["access_token"])
            user_info = sp.current_user()

            user, created = SpotifyUser.objects.get_or_create(
                spotify_id=user_info["id"]
            )

            images = user_info.get("images")
            if images:
                user.image = images[0]["url"]

            user.display_name = user_info.get("display_name")
            user.access_token = token_info["access_token"]
            user.access_token_expires_at = token_info["expires_at"]
            user.refresh_token = token_info["refresh_token"]
            user.save()
        except SpotifyOauthError:
            raise ValidationError(
                _("Authentication code is invalid. Please try again.")
            )

        auth_token, created = Token.objects.get_or_create(user=user)
        return Response({"auth_token": auth_token})
