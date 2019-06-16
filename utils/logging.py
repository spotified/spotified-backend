# -*- coding: utf-8 -*-
import logging
from collections import namedtuple

from django.conf import settings as s

LEVEL = namedtuple("LEVEL", ["DEBUG", "INFO", "WARNING", "ERROR"])
LEVEL = LEVEL(logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR)

logger = logging.getLogger(s.LOGGER_NAME)


def log(app_name, action, text, count=None, exc_info=False, level=LEVEL.INFO):
    logger.log(level, text, exc_info=exc_info, extra={"tags": {"app_name": app_name, "action": action, "count": count}})
