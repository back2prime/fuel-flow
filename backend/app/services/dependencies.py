from typing import Annotated

from fastapi import Depends

from app.services.tankerkoenig import TankerkoenigService
from core.helpers.http_helper import http_helper
from core.helpers.redis_helper import redis_helper


def get_tankerkoenig_service() -> TankerkoenigService:
    return TankerkoenigService(http_helper=http_helper, redis_helper=redis_helper)


TankerkoenigDep = Annotated[TankerkoenigService, Depends(get_tankerkoenig_service)]
