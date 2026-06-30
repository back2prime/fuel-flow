from slowapi import Limiter
from core.config import settings
from fastapi import Request


def get_real_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host


limiter = Limiter(key_func=get_real_ip, storage_uri=settings.redis.url)
