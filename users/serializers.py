from django.contrib.auth import get_user_model
from rest_framework import serializers

SpotifyUser = get_user_model()


class SpotifyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyUser
        fields = ("spotify_id", "display_name", "image", "created", "modified")
