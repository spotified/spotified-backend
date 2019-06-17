# -*- coding: utf-8 -*-
from django.apps import AppConfig


class DjarnishAppConfig(AppConfig):
    name = "djarnish"
    verbose_name = "Django varnish helper"

    def ready(self):
        from . import model_observer  # noqa
