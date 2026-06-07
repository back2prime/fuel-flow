from typing import Any


import jwt

from core.helpers.http_helper import http_helper


class JwtHelper:
    """JWT helper for encoding and decoding tokens
    using symmetric algorithms (e.g. HS256)."""

    def __init__(self, key: str, algorithm: str | None):
        self._key = key
        self._algorithm = algorithm

    def encode(self, payload: dict[str, Any]) -> str:
        return jwt.encode(payload=payload, key=self._key, algorithm=self._algorithm)

    def decode(self, token: str) -> Any:
        return jwt.decode(jwt=token, key=self._key, algorithms=[self._algorithm])


jwt_helper = JwtHelper(key=http_helper._apikey, algorithm="HS256")
