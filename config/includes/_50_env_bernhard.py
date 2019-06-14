from config.includes import _20_credentials as c

BASE_URL = "http://127.0.0.1:8000"
SPOTIFY_API_AUTH_REDIRECT_URL = "http://127.0.0.1:8000/"

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
