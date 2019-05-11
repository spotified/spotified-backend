from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField
from django_extensions.db.models import TimeStampedModel


class Artist(models.Model):
    spotify_id = models.CharField(
        _("SpotifyID"), max_length=255, blank=False, null=False, unique=True
    )
    name = models.CharField(_("Name"), max_length=255, blank=False, null=False)


class Track(models.Model):
    spotify_id = models.CharField(
        _("SpotifyID"), max_length=255, blank=False, null=False, unique=True
    )
    name = models.CharField(_("Name"), max_length=255, blank=False, null=False)
    artists = models.ManyToManyField(Artist, blank=True)


class Playlist(TimeStampedModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False
    )
    name = models.CharField(
        _("Name"), max_length=255, blank=False, null=False, unique=True
    )
    tracks = models.ManyToManyField(Track, through="PlaylistTracks")


class PlaylistTracks(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)

    points = models.BigIntegerField(_("Points"), default=1)
    date_added = CreationDateTimeField(_("added"))

    class Meta:
        unique_together = ("playlist", "track")
