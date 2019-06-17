# -*- coding: utf-8 -*-
import re

from django.apps import apps
from django.db.models.signals import post_save
from djarnish.varnish import purge


def purge_model(sender, instance, created, **kwargs):
    if created:  # new content => no cached pages
        return

    if not instance.tracker.changed():
        return

    # build list of urls to purge
    observed_objs = getattr(instance._meta, "djarnish_observed", [])
    if type(observed_objs) == str:
        observed_objs = (observed_objs,)

    urls_to_purge = []
    for observed_obj in observed_objs:
        urls_to_purge.append(
            # escape url because we build a regex with
            re.escape(str(getattr(instance, observed_obj)()))
        )

    # build a regex of urls to purge multiple urls with one purge call
    urls_to_purge = "^({0})$".format("|".join(urls_to_purge))
    purge(urls_to_purge)


for model in apps.get_models():
    if hasattr(model._meta, "djarnish_observed"):
        post_save.connect(purge_model, sender=model)
