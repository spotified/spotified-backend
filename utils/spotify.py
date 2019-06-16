from urllib.parse import urlparse

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


def spotify_uri_or_link_to_id(uri_link_or_id, content_type):
    uri_link_or_id = uri_link_or_id.strip()

    if uri_link_or_id.lower().startswith("spotify:"):
        if not uri_link_or_id.lower().startswith("spotify:{}:".format(content_type)):
            raise ValidationError({"spotify_id": _("This is not a Spotify {} URI".format(content_type))})
        # e.g. spotify:track:6BBFXxmgCpkt5wfSSdeirq => 6BBFXxmgCpkt5wfSSdeirq
        return uri_link_or_id[14:]
    elif uri_link_or_id.lower().startswith("https://") or uri_link_or_id.lower().startswith("http://"):
        # e.g. https://open.spotify.com/track/6BBFXxmgCpkt5wfSSdeirq?si=JGFW4tlvQYGJWVMP9aBdVQ => 6BBFXxmgCpkt5wfSSdeirq
        url_pathes_parsed = urlparse(uri_link_or_id).path.split("/")

        try:
            if not url_pathes_parsed[-2] == content_type:
                raise ValidationError({"spotify_id": _("This is not a Spotify {} Link".format(content_type))})
            return url_pathes_parsed[-1]
        except IndexError:
            raise ValidationError({"spotify_id": _("This is not a Spotify {} Link".format(content_type))})
    else:
        return uri_link_or_id
