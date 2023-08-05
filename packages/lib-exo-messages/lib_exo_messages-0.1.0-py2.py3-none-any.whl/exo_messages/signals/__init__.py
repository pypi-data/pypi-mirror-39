from django.contrib.auth.signals import user_logged_in

from .signals_user_logged_handler import user_logged_handler


def setup_signals():
    user_logged_in.connect(user_logged_handler)
