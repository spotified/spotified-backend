# Generated by Django 2.2.2 on 2019-06-16 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("playlists", "0002_auto_20190614_1630")]

    operations = [migrations.RemoveField(model_name="track", name="artists"), migrations.DeleteModel(name="Artist")]
