import uuid
from typing import Any
import jwt
from core.helpers.http_helper import http_helper


class JwtHelper:
    """Thin wrapper around PyJWT for encoding and decoding application JWTs.

    Injects a unique jti claim on encode for blacklist support.
    Uses HS256 with the API key as the signing secret.
    """

    def __init__(self, key: str, algorithm: str | None):
        self._key = key
        self._algorithm = algorithm

    def encode(self, payload: dict[str, Any]) -> str:
        payload["jti"] = str(uuid.uuid4())
        return jwt.encode(payload=payload, key=self._key, algorithm=self._algorithm)

    def decode(self, token: str) -> Any:
        return jwt.decode(jwt=token, key=self._key, algorithms=[self._algorithm])


jwt_helper = JwtHelper(key=http_helper._apikey, algorithm="HS256")
