from core.schemes.base_schema import FrozenModelType


class TokenScheme(FrozenModelType):
    access_token: str
    token_type: str
