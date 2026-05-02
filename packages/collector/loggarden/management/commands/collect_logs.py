from django.core.management.base import BaseCommand
from loggarden.worker import LogWorker


class Command(BaseCommand):
    help = "Run LogGarden worker"

    def handle(self, *args, **kwargs):
        worker = LogWorker()
        worker.run()