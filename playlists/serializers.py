from rest_framework import serializers

from .models import Artist, Playlist, Track


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ("pk", "name", "owner")


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ("spotify_id", "name", "artists")


class ArtistSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance, _ = Artist.objects.get_or_create(**validated_data)
        return instance

    class Meta:
        model = Artist
        fields = ("spotify_id", "name")
