from django.apps import AppConfig


class Config(AppConfig):
    name = "articles"

    def ready(self):
        from . import signals  # noqa
