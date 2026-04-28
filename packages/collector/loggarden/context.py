from contextvars import ContextVar

_request_context: ContextVar[dict] = ContextVar("loggarden_context", default={})


def set_context(**kwargs):
    ctx = _request_context.get().copy()
    ctx.update(kwargs)
    _request_context.set(ctx)


def get_context() -> dict:
    return _request_context.get()


def clear_context():
    _request_context.set({})