from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from loggarden.models import LogEntry
from django.conf import settings


class Command(BaseCommand):
    help = "Delete old logs based on retention policy"

    def handle(self, *args, **kwargs):
        days = getattr(settings, "LOGGARDEN_RETENTION_DAYS", 15)
        batch_size = 5000

        cutoff = timezone.now() - timedelta(days=days)

        while True:
            qs = LogEntry.objects.filter(timestamp__lt=cutoff)[:batch_size]
            count = qs.count()
            if count == 0:
                break

            qs.delete()
            self.stdout.write(f"Deleted batch of {count}")