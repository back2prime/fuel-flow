from core.schemes.base_scheme import FrozenModelType

from typing import Literal


class StatusScheme(FrozenModelType):
    status: Literal["ok"]
