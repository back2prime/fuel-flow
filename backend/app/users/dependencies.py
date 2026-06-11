from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select

from app.database.dependencies import SessionDep
from app.users.models.users import User
from core.helpers.jwt_helper import jwt_helper
from core.helpers.redis_helper import redis_helper

security = HTTPBearer()


async def get_current_user(
    session: SessionDep, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    try:
        payload = jwt_helper.decode(token=credentials.credentials)
    except jwt.exceptions.PyJWTError:
        raise HTTPException(status_code=401, detail="Token was expired")

    jti = str(payload["jti"])

    is_blacklisted = await redis_helper.get(key=jti)
    if is_blacklisted is not None:
        raise HTTPException(status_code=403, detail="Token is invalid")

    user_id = payload["sub"]
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    try:
        return jwt_helper.decode(token=credentials.credentials)
    except jwt.exceptions.PyJWTError:
        raise HTTPException(status_code=401, detail="Token was expired")


TokenPayload = Annotated[dict, Depends(get_token_payload)]
CurrentUser = Annotated[User, Depends(get_current_user)]
