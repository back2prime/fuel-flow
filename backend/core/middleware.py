from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class LimitBodySizeMiddleware(BaseHTTPMiddleware):
    """Middleware that rejects requests exceeding a configured body size limit.

    Returns HTTP 413 if the Content-Length header exceeds max_body_size bytes.
    """
    def __init__(self, app, max_body_size: int):
        super().__init__(app)
        self.max_body_size = max_body_size

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("Content-Length")

        if content_length and int(content_length) > self.max_body_size:
            return Response(status_code=413)

        return await call_next(request)
