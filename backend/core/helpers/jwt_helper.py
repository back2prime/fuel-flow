import uuid
from typing import Any
import jwt
from core.helpers.http_helper import http_helper


class JwtHelper:
    def __init__(self, key: str, algorithm: str | None):
        self._key = key
        self._algorithm = algorithm

    def encode(self, payload: dict[str, Any]) -> str:
        payload["jti"] = str(uuid.uuid4())
        return jwt.encode(payload=payload, key=self._key, algorithm=self._algorithm)

    def decode(self, token: str) -> Any:
        return jwt.decode(jwt=token, key=self._key, algorithms=[self._algorithm])


jwt_helper = JwtHelper(key=http_helper._apikey, algorithm="HS256")
