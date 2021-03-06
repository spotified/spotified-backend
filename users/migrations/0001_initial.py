# Generated by Django 2.2.1 on 2019-05-10 19:05

import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SpotifyUser",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name="modified"),
                ),
                ("spotify_id", models.CharField(editable=False, max_length=255, unique=True, verbose_name="SpotifyID")),
                (
                    "display_name",
                    models.CharField(editable=False, max_length=255, null=True, verbose_name="Display name"),
                ),
                ("image", models.URLField(editable=False, max_length=1024, null=True, verbose_name="Image")),
                ("is_admin", models.BooleanField(default=False)),
                (
                    "access_token",
                    models.CharField(editable=False, max_length=255, null=True, verbose_name="Access Token"),
                ),
                (
                    "access_token_expires_at",
                    models.IntegerField(editable=False, null=True, verbose_name="Access Token Expires at"),
                ),
                (
                    "refresh_token",
                    models.CharField(editable=False, max_length=255, null=True, verbose_name="Refresh Token"),
                ),
            ],
            options={"abstract": False},
        )
    ]
