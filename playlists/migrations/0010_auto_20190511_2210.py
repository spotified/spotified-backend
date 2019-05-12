# Generated by Django 2.2.1 on 2019-05-11 20:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("playlists", "0009_auto_20190511_1715"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlaylistTrackVote",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "vote",
                    models.SmallIntegerField(choices=[(1, "vote +1"), (-1, "vote -1")]),
                ),
            ],
        ),
        migrations.RenameModel(old_name="PlaylistTracks", new_name="PlaylistTrack"),
        migrations.DeleteModel(name="TrackVote"),
        migrations.AddField(
            model_name="playlisttrackvote",
            name="playlist_track",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="playlists.PlaylistTrack",
            ),
        ),
        migrations.AddField(
            model_name="playlisttrackvote",
            name="voter",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterUniqueTogether(
            name="playlisttrackvote", unique_together={("voter", "playlist_track")}
        ),
    ]