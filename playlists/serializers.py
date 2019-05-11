from rest_framework import serializers

from .models import Artist, Playlist, Track


class ArtistSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance, _ = Artist.objects.get_or_create(**validated_data)
        return instance

    class Meta:
        model = Artist
        fields = ("spotify_id", "name")


class TrackSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True)

    class Meta:
        model = Track
        fields = ("spotify_id", "name", "artists")


class PlaylistSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Playlist
        fields = ("pk", "name", "owner", "tracks")
