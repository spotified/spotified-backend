# Generated by Django 2.2.1 on 2019-06-14 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("users", "0003_remove_spotifyuser_access_token_expires_at")]

    operations = [
        migrations.RenameField(
            model_name="spotifyuser", old_name="access_token_expires_at_dt", new_name="access_token_expires_at"
        )
    ]
