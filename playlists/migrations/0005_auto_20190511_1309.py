# Generated by Django 2.2.1 on 2019-05-11 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("playlists", "0004_auto_20190511_1306")]

    operations = [
        migrations.AddField(
            model_name="playlist",
            name="tracks",
            field=models.ManyToManyField(
                through="playlists.PlaylistTracks", to="playlists.Track"
            ),
        ),
        migrations.AddField(
            model_name="track",
            name="artists",
            field=models.ManyToManyField(blank=True, to="playlists.Artist"),
        ),
    ]
