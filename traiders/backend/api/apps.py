from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        from .signal_handlers import prediction_signals
        from .signal_handlers import parity_signal_handlers
