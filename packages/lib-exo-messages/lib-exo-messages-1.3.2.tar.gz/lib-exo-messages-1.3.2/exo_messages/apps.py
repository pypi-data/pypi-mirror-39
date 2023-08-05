from django.apps import AppConfig


class ExoMessagesConfig(AppConfig):
    name = 'exo_messages'

    def ready(self):
        from .signals import setup_signals
        setup_signals()
