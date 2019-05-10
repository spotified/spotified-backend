from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class Playlist(TimeStampedModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False
    )
    name = models.CharField(
        _("Name"), max_length=255, blank=False, null=False, unique=True
    )
