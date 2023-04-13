from django.apps import AppConfig


class ComicsConfig(AppConfig):

    name = 'Comics'

    def ready(self):
        from . import signals
