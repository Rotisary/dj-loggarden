# dj-loggarden

A Django-native log collector that stores structured logs in your database, with support for filtering by user, request, and context. Comes with an optional FastAPI viewer UI for querying logs.

## Features

- Structured log storage (PostgreSQL recommended)
- Supports Python `logging` and Loguru
- Automatic request and user context tracking
- Query logs by:
  - user_id
  - request_id
  - level
  - time range
- Django Admin integration (out of the box)
- Optional FastAPI-based log viewer API
- Batch ingestion for performance

---
