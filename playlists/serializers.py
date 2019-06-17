from collections import defaultdict

from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Playlist, PlaylistTag, PlaylistTrackVote, Track


class TrackSerializer(serializers.ModelSerializer):
    votes = serializers.DictField()

    class Meta:
        model = Track
        fields = ("pk", "spotify_id", "votes")


class SpotifyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("spotify_id",)


class PlaylistTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistTag
        fields = ("pk", "name")

    def create(self, validated_data):
        instance, _ = PlaylistTag.objects.get_or_create(**validated_data)
        return instance

    def validate_name(self, value):
        if value:
            return value.lower().replace(" ", "")


class PlaylistWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ("pk", "name", "owner")


class PlaylistReadSerializer(serializers.ModelSerializer):
    tags = PlaylistTagSerializer(many=True)
    tracks = SerializerMethodField(read_only=True)

    class Meta:
        model = Playlist
        fields = ("pk", "spotify_id", "name", "tracks", "tags")

    def get_tracks(self, instance):
        if isinstance(instance, Playlist):
            tracks = instance.tracks_score_ordered

            # collect votes for playlist tracks
            votes = (
                PlaylistTrackVote.objects.filter(playlist_track__track__in=tracks)
                .values("playlist_track__pk", "vote")
                .annotate(votes=Count("vote"))
            )

            tracks_votes_dict = defaultdict(lambda: {"ups": 0, "downs": 0})

            for vote in votes:
                if vote["vote"] == PlaylistTrackVote.VOTE_UP:
                    tracks_votes_dict[vote["playlist_track__pk"]]["ups"] = vote["votes"]
                elif vote["vote"] == PlaylistTrackVote.VOTE_DOWN:
                    tracks_votes_dict[vote["playlist_track__pk"]]["downs"] = vote["votes"]

            for track in tracks:
                track.votes = tracks_votes_dict[track.pk]

            return TrackSerializer(tracks, many=True).data
        else:
            return []


class PlaylistTrackVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistTrackVote
        fields = ("pk", "voter", "playlist_track", "vote")
