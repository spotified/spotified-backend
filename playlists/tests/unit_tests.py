import os
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TransactionTestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from users.authentication import TokenAuthentication
from utils.spotify import spotify_uri_or_link_to_id

from ..models import Playlist, PlaylistTrack, Track

TESTS_FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")

SpotifyUser = get_user_model()


@override_settings(FIXTURE_DIRS=(TESTS_FIXTURES_DIR,))
class PlaylistTest(TransactionTestCase):
    fixtures = ["playlists.json"]

    def setUp(self):
        # patch request_fresh_access_token
        patcher = patch("users.models.SpotifyUser.request_fresh_access_token", return_value=True)
        self.request_fresh_access_token = patcher.start()
        self.addCleanup(patcher.stop)

        self.client = APIClient()

    def set_api_credentials(self, auth_token):
        self.client.credentials(HTTP_AUTHORIZATION="{} {}".format(TokenAuthentication.keyword, auth_token))

    @patch("spotipy.Spotify.user_playlist_create")
    def test_playlist_post(self, mock_user_playlist_create):
        playlist_name = "my playlist"
        user = SpotifyUser.objects.get(access_token="access_token")
        mock_user_playlist_create.return_value = {"id": "s_id", "snapshot_id": "s_snapshot_id"}

        self.set_api_credentials(user.access_token)

        # post with name empty
        response = self.client.post(reverse("api_v1:playlists:playlists"))
        self.assertEqual(response.status_code, 400)

        # create a new playlist
        response = self.client.post(reverse("api_v1:playlists:playlists"), {"name": playlist_name})
        self.assertEqual(response.status_code, 200)

        # test created playlist
        playlist = Playlist.objects.get(name=playlist_name)
        self.assertEqual(playlist.owner, user)
        self.assertEqual(playlist.spotify_id, mock_user_playlist_create.return_value["id"])
        self.assertEqual(playlist.spotify_snapshot_id, mock_user_playlist_create.return_value["snapshot_id"])

        # create playlist with same name again
        response = self.client.post(reverse("api_v1:playlists:playlists"), {"name": playlist_name})
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

        response = self.client.get(reverse("api_v1:playlists:playlist", kwargs={"playlist_id": playlist_pk}))
        self.assertEqual(response.status_code, 200)

        playlist = response.json()
        self.assertEquals(playlist["pk"], playlist_pk)

        # test 404
        response = self.client.get(reverse("api_v1:playlists:playlist", kwargs={"playlist_id": 9999}))
        self.assertEqual(response.status_code, 404)

    @patch("spotipy.Spotify.track")
    def test_playlist_track_add(self, mock_track):
        playlist_pk = 1
        self.set_api_credentials("access_token")

        # add by spotify URI and URL
        for spotify_track in [
            "spotify:track:1csLNQUyuhEPFiP1Qvjk9b",
            "http://open.spotify.com/track/3Kbriu0vdmCxd6iGDGBENw?si=lqHwG7qeSIaMYYXTS9f0Pw",
        ]:
            mock_track.return_value = {"id": spotify_track}

            response = self.client.post(
                reverse("api_v1:playlists:playlist_track", kwargs={"playlist_id": playlist_pk}),
                {"spotify_id": spotify_track},
            )
            self.assertEqual(response.status_code, 200)

            # test for saved object
            spotify_track_id = spotify_uri_or_link_to_id(spotify_track, content_type="track")
            track = Track.objects.get(spotify_id=spotify_track_id)
            self.assertEquals(PlaylistTrack.objects.filter(playlist__pk=playlist_pk, track=track).count(), 1)

            # try to add again
            response = self.client.post(
                reverse("api_v1:playlists:playlist_track", kwargs={"playlist_id": playlist_pk}),
                {"spotify_id": mock_track.return_value["id"]},
            )
            self.assertEqual(response.status_code, 400)

    @patch("spotipy.Spotify.track")
    def test_playlist_track_add_invalid_ids(self, mock_track):
        playlist_pk = 1
        self.set_api_credentials("access_token")

        mock_track.return_value = {"id": "spotify_track_id"}

        # 404 playlist add
        response = self.client.post(
            reverse("api_v1:playlists:playlist_track", kwargs={"playlist_id": 9999}), {"spotify_id": "spotify:foo"}
        )
        self.assertEqual(response.status_code, 404)

        # test invalid URI
        response = self.client.post(
            reverse("api_v1:playlists:playlist_track", kwargs={"playlist_id": playlist_pk}),
            {"spotify_id": "spotify:artist:"},
        )
        self.assertEqual(response.status_code, 400)

        # invalid url
        response = self.client.post(
            reverse("api_v1:playlists:playlist_track", kwargs={"playlist_id": playlist_pk}),
            {"spotify_id": "http://open.spotify.com/track"},
        )
        self.assertEqual(response.status_code, 400)

        # invalid spotify content
        response = self.client.post(
            reverse("api_v1:playlists:playlist_track", kwargs={"playlist_id": playlist_pk}),
            {"spotify_id": "http://open.spotify.com/artist/aaaa/"},
        )
        self.assertEqual(response.status_code, 400)

        # invalid local tracks
        mock_track.return_value = {"id": "spotify:track:1csLNQUyuhEPFiP1Qvjk9b", "is_local": True}
        response = self.client.post(
            reverse("api_v1:playlists:playlist_track", kwargs={"playlist_id": playlist_pk}),
            {"spotify_id": mock_track.return_value["id"]},
        )
        self.assertEqual(response.status_code, 400)

    def test_playlist_track_add_unauthorized(self):
        response = self.client.post(reverse("api_v1:playlists:playlist_track", kwargs={"playlist_id": 1}))
        self.assertEqual(response.status_code, 401)
