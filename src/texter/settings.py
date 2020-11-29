import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = True if os.getenv("DEBUG", "").lower() == "true" else False

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "rest_framework",
    "articles.apps.Config",
]

ROOT_URLCONF = "texter.urls"

WSGI_APPLICATION = "texter.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

# probably only one token is needed, there is no point in making db model for it
# in memory token-set will also run faster
EDITOR_TOKENS = set(os.getenv("EDITOR_TOKENS", "").split(","))

# disable DRF auth classes, they depend on Django apps which are not installed in
# this project for simplicity
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "UNAUTHENTICATED_USER": None,
}
