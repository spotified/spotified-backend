from rest_framework.views import APIView

HEADER_FIELD_X_AUTH_TOKEN_EXPIRES_AT = "X-AUTH-TOKEN-EXPIRES-AT"


class AuthTokenExpiresAtHeaderMixin(APIView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.user.is_authenticated and request.user.access_token:
            response[
                HEADER_FIELD_X_AUTH_TOKEN_EXPIRES_AT
            ] = request.user.access_token_expires_at.astimezone()
        return response
