from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Artist, Playlist, PlaylistTag, PlaylistTrackVote, Track


class ArtistSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance, _ = Artist.objects.get_or_create(**validated_data)
        return instance

    class Meta:
        model = Artist
        fields = ("spotify_id", "name")


class TrackSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True, read_only=True)

    class Meta:
        model = Track
        fields = ("spotify_id", "name", "artists")


class PlaylistSerializer(serializers.ModelSerializer):
    tracks = SerializerMethodField(read_only=True)

    class Meta:
        model = Playlist
        fields = ("pk", "name", "owner", "tracks")

    def get_tracks(self, instance):
        if isinstance(instance, Playlist):
            tracks = instance.tracks_score_ordered
            return TrackSerializer(tracks, many=True).data
        else:
            return None


class PlaylistOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ("pk", "name", "owner")


class PlaylistTrackVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistTrackVote
        fields = ("pk", "voter", "playlist_track", "vote")


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
