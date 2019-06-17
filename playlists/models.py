from decimal import Decimal
from math import exp, sqrt

from django.conf import settings
from django.db import models
from django.db.models import Count
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField
from django_extensions.db.models import TimeStampedModel
from model_utils import FieldTracker


class Track(models.Model):
    spotify_id = models.CharField(_("SpotifyID"), max_length=255, blank=False, null=False, unique=True)

    def __str__(self):
        return self.spotify_id


class PlaylistTag(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    count = models.IntegerField(default=0, help_text="Internal counter of how many times this tag is in use")

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Playlist(TimeStampedModel):
    spotify_id = models.CharField(_("SpotifyID"), max_length=255, blank=False, null=False, unique=True)
    spotify_snapshot_id = models.CharField(_("Spotify SnapshotID"), max_length=60, blank=False, null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(_("Name"), max_length=255, blank=False, null=False, unique=True)

    tracks = models.ManyToManyField(Track, through="PlaylistTrack")
    tags = models.ManyToManyField(PlaylistTag, blank=True)

    tracker = FieldTracker()

    class Meta:
        djarnish_observed = ("get_absolute_url",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("api_v1:playlists:playlist", args=[self.pk])

    @property
    def tracks_score_ordered(self):
        return self.tracks.all().order_by("-playlisttrack__score")

    def upload_to_spotify(self):
        response = self.owner.spotify_api.user_playlist_replace_tracks(
            self.owner.spotify_id, self.spotify_id, tracks=[track.spotify_id for track in self.tracks_score_ordered]
        )
        self.spotify_snapshot_id = response["snapshot_id"]
        self.save()


class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)

    score = models.DecimalField(_("Points"), decimal_places=4, max_digits=6)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)
    date_added = CreationDateTimeField(_("added"))

    tracker = FieldTracker()

    class Meta:
        unique_together = ("playlist", "track")
        ordering = ["score"]

    def calculate_score(self):
        """
        Based on: https://medium.com/hacking-and-gonzo/how-reddit-ranking-algorithms-work-ef111e33d0d9
        extended by submission time gravity
        """

        ups = 0
        downs = 0

        if not self.pk:
            submission_date = now()
        else:
            submission_date = self.date_added

            votes = self.playlisttrackvote_set.all().values("vote").annotate(votes=Count("vote"))

            for vote in votes:
                if vote["vote"] == PlaylistTrackVote.VOTE_UP:
                    ups = vote["votes"]
                elif vote["vote"] == PlaylistTrackVote.VOTE_DOWN:
                    downs = vote["votes"]

        score = 0
        submission_age = now() - submission_date

        if ups + downs != 0:
            n = ups + downs
            if n == 0:
                return 0

            z = 1.281551565545
            p = float(ups) / n

            left = p + 1 / (2 * n) * z * z
            right = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
            under = 1 + 1 / n * z * z

            score = (left - right) / under

        if submission_age.seconds < 172800:
            score += exp(-1 * (submission_age.seconds / 36000)) / max((downs - ups) / 5, 1)

        score = Decimal(score)
        self.score = score.quantize(Decimal(10) ** -PlaylistTrack._meta.get_field("score").decimal_places)

    def save(self, *args, **kwargs):
        self.calculate_score()

        if self.tracker.changed():
            super().save(*args, **kwargs)

            # set playlist modified and trigger playlist change
            self.playlist.save()


class PlaylistTrackVote(models.Model):
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)
    playlist_track = models.ForeignKey(PlaylistTrack, on_delete=models.CASCADE, blank=False, null=False)

    VOTE_UP = 1
    VOTE_DOWN = -1
    VOTE_CHOICES = ((VOTE_UP, "vote +1"), (VOTE_DOWN, "vote -1"))
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ("voter", "playlist_track")
