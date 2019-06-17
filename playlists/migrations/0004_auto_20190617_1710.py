# Generated by Django 2.2.2 on 2019-06-17 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("playlists", "0003_auto_20190616_1806")]

    operations = [
        migrations.AlterModelOptions(name="playlist", options={}),
        migrations.AlterField(
            model_name="playlisttrack",
            name="score",
            field=models.DecimalField(decimal_places=5, max_digits=7, verbose_name="Points"),
        ),
    ]
