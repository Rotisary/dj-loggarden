import uuid
from .context import set_context, clear_context


class LogGardenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            set_context(
                request_id=str(uuid.uuid4()),
                path=request.path,
                method=request.method,
                ip=self._get_ip(request),
                user_id=self._get_user_id(request),
            )

            response = self.get_response(request)
            return response

        finally:
            clear_context()

    def _get_ip(self, request):
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            return xff.split(",")[0]
        return request.META.get("REMOTE_ADDR")

    def _get_user_id(self, request):
        if hasattr(request, "user") and request.user.is_authenticated:
            return str(request.user.id)
        return None