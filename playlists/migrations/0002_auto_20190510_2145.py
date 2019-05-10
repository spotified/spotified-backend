# Generated by Django 2.2.1 on 2019-05-10 19:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("playlists", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="playlist",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        )
    ]
