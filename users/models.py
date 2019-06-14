from datetime import datetime, timedelta

import spotipy
from django.conf import settings as s
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.timezone import make_aware, now
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from spotipy import oauth2


class SpotifyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(username=self.normalize_email(username))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class SpotifyUser(AbstractBaseUser, TimeStampedModel):
    spotify_id = models.CharField(
        _("SpotifyID"),
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        editable=False,
    )
    display_name = models.CharField(
        _("Display name"), blank=False, null=True, max_length=255, editable=False
    )
    image = models.URLField(
        _("Image"), max_length=1024, blank=False, null=True, editable=False
    )

    is_admin = models.BooleanField(default=False)

    # OAuth stuff
    access_token = models.CharField(
        _("Access Token"),
        max_length=255,
        blank=False,
        null=True,
        editable=False,
        unique=True,
    )
    access_token_expires_at = models.DateTimeField(
        _("Access Token Expires at"), blank=False, null=True, editable=False
    )
    refresh_token = models.CharField(
        _("Refresh Token"), max_length=255, blank=False, null=True, editable=False
    )

    objects = SpotifyUserManager()
    USERNAME_FIELD = "spotify_id"

    SPOTIFY_API_SCOPES = "playlist-modify-public"

    oauth = oauth2.SpotifyOAuth(
        s.SPOTIFY_API_CLIENT_ID,
        s.SPOTIFY_API_CLIENT_SECRET,
        s.SPOTIFY_API_AUTH_REDIRECT_URL,
        scope=SPOTIFY_API_SCOPES,
    )

    def __str__(self):
        return self.spotify_id

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_token_expired(self):
        return now() - timedelta(seconds=60) > self.access_token_expires_at

    @property
    def spotify_api(self):
        if self.is_token_expired:
            self.request_fresh_access_token()
        return spotipy.Spotify(auth=self.access_token)

    def request_fresh_access_token(self):
        token_info = self.oauth.refresh_access_token(self.refresh_token)
        if token_info:
            self.access_token = token_info["access_token"]
            self.refresh_token = token_info["refresh_token"]
            self.access_token_expires_at = make_aware(
                datetime.fromtimestamp(token_info["expires_at"])
            )
            self.save()
            return True
        return False
