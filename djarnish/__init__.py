# -*- coding: utf-8 -*-
from django.db import models

models.options.DEFAULT_NAMES += ("djarnish_observed",)

default_app_config = "djarnish.apps.DjarnishAppConfig"
