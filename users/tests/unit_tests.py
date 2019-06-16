from unittest.mock import patch

from django.conf import settings as s
from django.contrib.auth import get_user_model
from django.test import Client, TransactionTestCase
from django.urls import reverse
from django.utils.timezone import now

SpotifyUser = get_user_model()


class SimpleTest(TransactionTestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_oauth_flow_start(self):
        response = self.client.get(reverse("api_v1:auth:start"))

        self.assertEqual(response.status_code, 200)

        # test oauth URL
        oauth_url = response.json()["url"]

        self.assertTrue(
            oauth_url.startswith("https://accounts.spotify.com/authorize"), True
        )
        self.assertIn("client_id={}".format(s.SPOTIFY_API_CLIENT_ID), oauth_url)
        self.assertIn("scope={}".format(SpotifyUser.SPOTIFY_API_SCOPES), oauth_url)

    @patch("users.models.SpotifyUser.oauth.get_access_token")
    @patch("spotipy.Spotify.current_user")
    def test_oauth_flow_finish_success(self, mock_current_user, mock_get_access_token):
        access_token_expires_at = now().replace(microsecond=0).astimezone()

        mock_get_access_token.return_value = {
            "access_token": "123-a",
            "expires_at": int(access_token_expires_at.strftime("%s")),
            "refresh_token": "123-r",
        }
        mock_current_user.return_value = {"id": "spotifyUserID"}

        response = self.client.post(
            reverse("api_v1:auth:finish"),
            {"code": "c"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        # test saved user
        u = SpotifyUser.objects.get(spotify_id=mock_current_user.return_value["id"])

        self.assertEquals(
            u.access_token, mock_get_access_token.return_value["access_token"]
        )
        self.assertEquals(
            u.refresh_token, mock_get_access_token.return_value["refresh_token"]
        )
        self.assertEquals(u.access_token_expires_at, access_token_expires_at)
