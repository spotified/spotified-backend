import sys

import raven
from config.includes import _20_credentials as c
from django.conf import settings as s

BASE_URL = "http://127.0.0.1:8000"

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": c.DB_NAME,
        "USER": c.DB_USER,
        "PASSWORD": c.DB_PASSWORD,
        "HOST": c.DB_HOST,
        "PORT": c.DB_PORT,
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Sentry
sentry_exceptions_to_ignore = (
    ["*"]
    if len(sys.argv) > 1 and sys.argv[1] in ["shell", "shell_plus"]
    else ["KeyboardInterrupt"]
)

RAVEN_CONFIG = {
    "dsn": c.RAVEN_DSN,
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    "release": raven.fetch_git_sha(s.BASE_DIR),
    "ignore_exceptions": sentry_exceptions_to_ignore,
}
