from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

from .management.commands.collect_logs import Command as CollectorCommand
from .management.commands.process_dlq import Command as DLQCommand
from .management.commands.cleanup_logs import Command as CleanupCommand

_scheduler = None


def start_scheduler():
    global _scheduler

    if _scheduler:
        return

    _scheduler = BackgroundScheduler()

    _scheduler.add_job(
        CollectorCommand().handle,
        "interval",
        seconds=getattr(settings, "LOGGARDEN_FLUSH_INTERVAL", 2),
    )

    _scheduler.add_job(
        DLQCommand().handle,
        "interval",
        seconds=getattr(settings, "LOGGARDEN_DLQ_INTERVAL", 300),
    )

    _scheduler.add_job(
        CleanupCommand().handle,
        "cron",
        hour=getattr(settings, "LOGGARDEN_CLEANUP_HOUR", 2),
    )

    _scheduler.start()