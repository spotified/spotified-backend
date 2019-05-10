LOGGER_NAME = "spotified"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "sentry": {
            "level": "INFO",
            "class": "raven.contrib.django.raven_compat.handlers.SentryHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {"propagate": False, "handlers": ["sentry", "console"]},
        "django.request": {
            "level": "ERROR",
            "propagate": False,
            "handlers": ["sentry", "console"],
        },
        "django.db.backends": {
            "level": "ERROR",
            "propagate": False,
            "handlers": ["sentry", "console"],
        },
        "raven": {
            "level": "WARNING",
            "propagate": False,
            "handlers": ["sentry", "console"],
        },
        "sentry.errors": {
            "level": "WARNING",
            "propagate": False,
            "handlers": ["sentry", "console"],
        },
        LOGGER_NAME: {
            "level": "INFO",
            "propagate": False,
            "handlers": ["sentry", "console"],
        },
        "{}.test".format(LOGGER_NAME): {
            "level": "INFO",
            "propagate": False,
            "handlers": ["console"],
        },
    },
}
