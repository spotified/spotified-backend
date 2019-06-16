import os
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TransactionTestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from users.authentication import TokenAuthentication

from ..models import Playlist

TESTS_FIXTURES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "fixtures"
)

SpotifyUser = get_user_model()


@override_settings(FIXTURE_DIRS=(TESTS_FIXTURES_DIR,))
class PlaylistTest(TransactionTestCase):
    fixtures = ["playlists.json"]

    def setUp(self):
        patcher = patch(
            "users.models.SpotifyUser.request_fresh_access_token", return_value=True
        )
        self.request_fresh_access_token = patcher.start()
        self.addCleanup(patcher.stop)

        self.client = APIClient()

    def set_api_credentials(self, auth_token):
        self.client.credentials(
            HTTP_AUTHORIZATION="{} {}".format(TokenAuthentication.keyword, auth_token)
        )

    @patch("spotipy.Spotify.user_playlist_create")
    def test_playlist_post_authorized(self, mock_user_playlist_create):
        playlist_name = "my playlist"
        user = SpotifyUser.objects.get(access_token="access_token")
        mock_user_playlist_create.return_value = {
            "id": "s_id",
            "snapshot_id": "s_snapshot_id",
        }

        self.set_api_credentials(user.access_token)

        # post with name empty
        response = self.client.post(reverse("api_v1:playlists:playlists"))
        self.assertEqual(response.status_code, 400)

        # create a new playlist
        response = self.client.post(
            reverse("api_v1:playlists:playlists"), {"name": playlist_name}
        )
        self.assertEqual(response.status_code, 200)

        # test created playlist
        playlist = Playlist.objects.get(name=playlist_name)
        self.assertEqual(playlist.owner, user)
        self.assertEqual(
            playlist.spotify_id, mock_user_playlist_create.return_value["id"]
        )
        self.assertEqual(
            playlist.spotify_snapshot_id,
            mock_user_playlist_create.return_value["snapshot_id"],
        )

        # create playlist with same name again
        response = self.client.post(
            reverse("api_v1:playlists:playlists"), {"name": playlist_name}
        )
        self.assertEqual(response.status_code, 400)

    def test_playlist_post_unauthorized(self):
        response = self.client.post(reverse("api_v1:playlists:playlists"))
        self.assertEqual(response.status_code, 401)

    def test_playlist_get_all(self):
        response = self.client.get(reverse("api_v1:playlists:playlists"))
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(response.json()), 2)

    def test_playlist_get_single(self):
        playlist_pk = 1
        response = self.client.get(
            reverse("api_v1:playlists:playlist", kwargs={"playlist_id": playlist_pk})
        )
        self.assertEqual(response.status_code, 200)

        playlist = response.json()
        self.assertEquals(playlist["pk"], playlist_pk)
