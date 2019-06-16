from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Playlist, PlaylistTag, PlaylistTrackVote, Track


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ("pk", "spotify_id")


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
            return value.lower()


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
            return TrackSerializer(tracks, many=True).data
        else:
            return None


class PlaylistTrackVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistTrackVote
        fields = ("pk", "voter", "playlist_track", "vote")
