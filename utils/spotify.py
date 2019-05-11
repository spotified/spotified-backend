from urllib.parse import urlparse

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


def spotify_uri_or_link_to_id(uri_or_link):
    uri_or_link = uri_or_link.strip()

    if uri_or_link.lower().startswith("spotify:"):
        if not uri_or_link.lower().startswith("spotify:track:"):
            raise ValidationError({"spotify_id": _("This is not a Spotify Track URI")})
        # e.g. spotify:track:6BBFXxmgCpkt5wfSSdeirq => 6BBFXxmgCpkt5wfSSdeirq
        return uri_or_link[14:]
    elif uri_or_link.lower().startswith("https://") or uri_or_link.lower().startswith(
        "http://"
    ):
        # e.g. https://open.spotify.com/track/6BBFXxmgCpkt5wfSSdeirq?si=JGFW4tlvQYGJWVMP9aBdVQ => JGFW4tlvQYGJWVMP9aBdVQ
        url_pathes_parsed = urlparse(uri_or_link).path.split("/")

        try:
            if not url_pathes_parsed[-2] == "track":
                raise ValidationError(
                    {"spotify_id": _("This is not a Spotify Track Link")}
                )
            return url_pathes_parsed[-1]
        except IndexError:
            raise ValidationError({"spotify_id": _("This is not a Spotify Track Link")})

    raise ValidationError({"spotify_id": _("Spotify TrackID format unknown")})
