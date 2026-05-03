from django.db import models
from django.conf import settings


class LogEntry(models.Model):
    timestamp = models.DateTimeField(db_index=True)
    level = models.CharField(max_length=32, db_index=True)
    message = models.TextField()
    logger_name = models.CharField(max_length=255)

    user_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    request_id = models.CharField(max_length=128, blank=True, null=True, db_index=True)

    path = models.TextField(blank=True, null=True)
    method = models.CharField(max_length=16, blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)

    module = models.CharField(max_length=255, blank=True)
    function = models.CharField(max_length=255, blank=True)
    line = models.PositiveIntegerField(blank=True, null=True)
    file = models.TextField(blank=True)

    exception_type = models.CharField(max_length=255, blank=True, null=True)
    exception_message = models.TextField(blank=True, null=True)
    traceback = models.TextField(blank=True, null=True)

    extra = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        ordering = ["-timestamp", "-id"]
        indexes = [
            models.Index(fields=["-timestamp"], name="logentry_ts_desc_idx"),
            models.Index(fields=["user_id", "-timestamp"], name="logentry_user_ts_idx"),
            models.Index(fields=["request_id"], name="logentry_request_idx"),
            models.Index(fields=["level", "-timestamp"], name="logentry_level_ts_idx"),
        ]

        if "postgresql" in settings.DATABASES["default"]["ENGINE"]:
            from django.contrib.postgres.indexes import GinIndex

            indexes.append(
                GinIndex(fields=["extra"], name="logentry_extra_gin_idx")
            )

    def __str__(self) -> str:
        return f"[{self.level}] {self.logger_name}: {self.message[:80]}"
