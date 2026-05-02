from django.core.management.base import BaseCommand
from loggarden.worker import LogWorker
from loggarden.queue.redis import DeadLetterQueue


class Command(BaseCommand):
    help = "Reprocess failed logs from DLQ"

    def handle(self, *args, **kwargs):
        dlq = DeadLetterQueue()
        worker = LogWorker()

        while True:
            batch = dlq.dequeue_batch(worker.batch_size)

            if not batch:
                self.stdout.write("DLQ empty")
                break

            worker._process_batch(batch)