from rest_framework.views import APIView

HEADER_FIELD_X_SPOTIFY_TOKEN_EXPIRES_AT = "X-SPOTIFY-TOKEN-EXPIRES-AT"


class SpotifyTokenExpiresAtHeaderMixin(APIView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.user.is_authenticated and request.user.access_token:
            response[
                HEADER_FIELD_X_SPOTIFY_TOKEN_EXPIRES_AT
            ] = request.user.access_token_expires_at.astimezone()
        return response