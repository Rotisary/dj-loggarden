import django.contrib.postgres.indexes
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LogEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("timestamp", models.DateTimeField(db_index=True)),
                ("level", models.CharField(db_index=True, max_length=32)),
                ("message", models.TextField()),
                ("logger_name", models.CharField(max_length=255)),
                ("user_id", models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ("request_id", models.CharField(blank=True, db_index=True, max_length=128, null=True)),
                ("path", models.TextField(blank=True)),
                ("method", models.CharField(blank=True, max_length=16)),
                ("ip", models.GenericIPAddressField(blank=True, null=True)),
                ("module", models.CharField(blank=True, max_length=255)),
                ("function", models.CharField(blank=True, max_length=255)),
                ("line", models.PositiveIntegerField(blank=True, null=True)),
                ("file", models.TextField(blank=True)),
                ("exception_type", models.CharField(blank=True, max_length=255)),
                ("exception_message", models.TextField(blank=True)),
                ("traceback", models.TextField(blank=True)),
                ("extra", models.JSONField(blank=True, default=dict)),
            ],
            options={
                "ordering": ["-timestamp", "-id"],
                "indexes": [
                    models.Index(fields=["-timestamp"], name="logentry_ts_desc_idx"),
                    models.Index(fields=["user_id", "-timestamp"], name="logentry_user_ts_idx"),
                    models.Index(fields=["request_id"], name="logentry_request_idx"),
                    models.Index(fields=["level", "-timestamp"], name="logentry_level_ts_idx"),
                    django.contrib.postgres.indexes.GinIndex(fields=["extra"], name="logentry_extra_gin_idx"),
                ],
            },
        ),
    ]
