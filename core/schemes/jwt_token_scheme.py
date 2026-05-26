from core.schemes import FrozenModelType


class TokenScheme(FrozenModelType):
    access_token: str
    token_type: str