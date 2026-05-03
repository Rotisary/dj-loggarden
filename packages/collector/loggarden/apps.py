from django.apps import AppConfig
import os


class LoggardenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "loggarden"

    def ready(self):
        if os.environ.get("RUN_MAIN") != "true":
            return

        from django.conf import settings

        if getattr(settings, "LOGGARDEN_AUTOSTART", True):
            from .scheduler import start_scheduler
            start_scheduler()