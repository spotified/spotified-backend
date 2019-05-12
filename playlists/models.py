from datetime import datetime
from math import log

import pytz
from django.conf import settings
from django.db import models
from django.utils.timezone import get_default_timezone_name, now
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
    tracks = models.ManyToManyField(Track, through="PlaylistTrack")

    @property
    def tracks_score_ordered(self):
        return self.tracks.all().order_by("-playlisttrack__score")


class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)

    score = models.DecimalField(_("Points"), decimal_places=7, max_digits=12)
    date_added = CreationDateTimeField(_("added"))

    class Meta:
        unique_together = ("playlist", "track")
        ordering = ["score"]

    def calculate_score(self):
        """
        Based on:
        https://medium.com/hacking-and-gonzo/how-reddit-ranking-algorithms-work-ef111e33d0d9
        """

        epoch = pytz.timezone(get_default_timezone_name()).localize(
            datetime(1970, 1, 1)
        )

        def epoch_seconds(date):
            td = date - epoch
            return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

        if not self.pk:
            ups = 0
            downs = 0
            date = now()
        else:
            ups = PlaylistTrackVote.objects.filter(
                playlist_track=self, vote=PlaylistTrackVote.VOTE_UP
            ).count()
            downs = PlaylistTrackVote.objects.filter(
                playlist_track=self, vote=PlaylistTrackVote.VOTE_DOWN
            ).count()
            date = self.date_added

        s = ups - downs
        order = log(max(abs(s), 1), 10)
        sign = 1 if s > 0 else -1 if s < 0 else 0
        seconds = epoch_seconds(date) - 1134028003
        return round(sign * order + seconds / 45000, 7)

    def save(self, *args, **kwargs):
        self.score = self.calculate_score()
        super().save(*args, **kwargs)


class PlaylistTrackVote(models.Model):
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False
    )
    playlist_track = models.ForeignKey(
        PlaylistTrack, on_delete=models.CASCADE, blank=False, null=False
    )

    VOTE_UP = 1
    VOTE_DOWN = -1
    VOTE_CHOICES = ((VOTE_UP, "vote +1"), (VOTE_DOWN, "vote -1"))
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ("voter", "playlist_track")
