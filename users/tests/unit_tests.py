import os
from unittest.mock import patch

from django.conf import settings as s
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase, override_settings
from django.urls import reverse
from django.utils.timezone import now
from rest_framework.test import APIClient

from ..authentication import TokenAuthentication

TESTS_FIXTURES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "fixtures"
)

SpotifyUser = get_user_model()


@override_settings(FIXTURE_DIRS=(TESTS_FIXTURES_DIR,))
class UserTest(TransactionTestCase):
    fixtures = ["users.json"]

    def setUp(self):
        # Every test needs a client.
        self.client = APIClient(format="json")

    def set_api_credentials(self, auth_token):
        self.client.credentials(
            HTTP_AUTHORIZATION="{} {}".format(TokenAuthentication.keyword, auth_token)
        )

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

        response = self.client.post(reverse("api_v1:auth:finish"), {"code": "c"})
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

    @patch("spotipy.oauth2.SpotifyOAuth.refresh_access_token")
    def test_oauth_token_refresh_authorized(self, mock_request_fresh_access_token):
        access_token_expires_at = now().replace(microsecond=0).astimezone()

        mock_request_fresh_access_token.return_value = {
            "access_token": "123-a",
            "expires_at": int(access_token_expires_at.strftime("%s")),
            "refresh_token": "123-r",
        }

        self.set_api_credentials("access_token")

        response = self.client.post(reverse("api_v1:auth:auth_token_refresh"))
        self.assertEqual(response.status_code, 200)

        # test updated token info
        u = SpotifyUser.objects.get(spotify_id="spotify_id")

        self.assertEquals(
            u.access_token, mock_request_fresh_access_token.return_value["access_token"]
        )
        self.assertEquals(
            u.refresh_token,
            mock_request_fresh_access_token.return_value["refresh_token"],
        )
        self.assertEquals(u.access_token_expires_at, access_token_expires_at)

        # test new token
        self.set_api_credentials(
            mock_request_fresh_access_token.return_value["access_token"]
        )

        response = self.client.post(reverse("api_v1:auth:auth_token_refresh"))
        self.assertEqual(response.status_code, 200)

    def test_oauth_token_refresh_unauthorized(self):
        response = self.client.post(reverse("api_v1:auth:auth_token_refresh"))
        self.assertEqual(response.status_code, 401)
